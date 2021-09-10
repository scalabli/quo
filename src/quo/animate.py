from typing import cast, List, Optional, TYPE_CHECKING

from quo.animation import ANIMATION
from .measure import Measurement
from .tabulate import Table
from quo.text import Text

if TYPE_CHECKING:
    from .terminal import Terminal, ConsoleOptions, RenderResult, RenderableType
    from .style import StyleType


class Animate:
    def __init__(
        self,
        name: str,
        text: "RenderableType" = "",
        *,
        style: Optional["StyleType"] = None,
        speed: float = 1.0,
    ) -> None:
        """A spinner animation.

        Args:
            name (str): Name of spinner (run python -m rich.spinner).
            text (RenderableType, optional): A renderable to display at the right of the spinner (str or Text typically). Defaults to "".
            style (StyleType, optional): Style for spinner animation. Defaults to None.
            speed (float, optional): Speed factor for animation. Defaults to 1.0.

        Raises:
            KeyError: If name isn't one of the supported spinner animations.
        """
        try:
            animate = ANIMATION[name]
        except KeyError:
            raise KeyError(f"no animation called {name!r}")
        self.text = Text.from_markup(text) if isinstance(text, str) else text
        self.frames = cast(List[str], animate["frames"])[:]
        self.interval = cast(float, animate["interval"])
        self.start_time: Optional[float] = None
        self.style = style
        self.speed = speed
        self.frame_no_offset: float = 0.0
        self._update_speed = 0.0

    def __rich_console__(
        self, console: "Terminal", options: "ConsoleOptions"
    ) -> "RenderResult":
        yield self.render(console.get_time())

    def __rich_measure__(
        self, console: "Terminal", options: "ConsoleOptions"
    ) -> Measurement:
        text = self.render(0)
        return Measurement.get(console, options, text)

    def render(self, time: float) -> "RenderableType":
        """Render the spinner for a given time.

        Args:
            time (float): Time in seconds.

        Returns:
            RenderableType: A renderable containing animation frame.
        """
        if self.start_time is None:
            self.start_time = time

        frame_no = ((time - self.start_time) * self.speed) / (
            self.interval / 1000.0
        ) + self.frame_no_offset
        frame = Text(
            self.frames[int(frame_no) % len(self.frames)], style=self.style or ""
        )

        if self._update_speed:
            self.frame_no_offset = frame_no
            self.start_time = time
            self.speed = self._update_speed
            self._update_speed = 0.0

        if not self.text:
            return frame
        elif isinstance(self.text, (str, Text)):
            return Text.assemble(frame, " ", self.text)
        else:
            table = Table.grid(padding=1)
            table.add_row(frame, self.text)
            return table

    def update(
        self,
        *,
        text: "RenderableType" = "",
        style: Optional["StyleType"] = None,
        speed: Optional[float] = None,
    ) -> None:
        """Updates attributes of a spinner after it has been started.

        Args:
            text (RenderableType, optional): A renderable to display at the right of the spinner (str or Text typically). Defaults to "".
            style (StyleType, optional): Style for spinner animation. Defaults to None.
            speed (float, optional): Speed factor for animation. Defaults to None.
        """
        if text:
            self.text = Text.from_markup(text) if isinstance(text, str) else text
        if style:
            self.style = style
        if speed:
            self._update_speed = speed


if __name__ == "__main__":  # pragma: no cover
    from time import sleep

    from .columns import Columns
    from .panel import Panel
    from .live import Live

    all_spinners = Columns(
        [
            Spinner(spinner_name, text=Text(repr(spinner_name), style="green"))
            for spinner_name in sorted(ANIMATION.keys())
        ],
        column_first=True,
        expand=True,
    )

    with Live(
        Panel(all_spinners, title="Animations", border_style="green"),
        refresh_per_second=20,
    ) as live:
        while True:
            sleep(0.1)
