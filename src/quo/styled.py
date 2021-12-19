from typing import TYPE_CHECKING

from quo.width import Measurement
from .segment import Segment
from .style import StyleType

if TYPE_CHECKING:
    from .terminal import Terminal, ConsoleOptions, RenderResult, RenderableType


class Styled:
    """Apply a style to a renderable.

    Args:
        renderable (RenderableType): Any renderable.
        style (StyleType): A style to apply across the entire renderable.
    """

    def __init__(self, renderable: "RenderableType", style: "StyleType") -> None:
        self.renderable = renderable
        self.style = style

    def __quo_console__(
        self, console: "Terminal", options: "ConsoleOptions"
    ) -> "RenderResult":
        style = console.get_style(self.style)
        rendered_segments = console.render(self.renderable, options)
        segments = Segment.apply_style(rendered_segments, style)
        return segments

    def __quo_measure__(
        self, console: "Terminal", options: "ConsoleOptions"
    ) -> Measurement:
        return Measurement.get(console, options, self.renderable)


if __name__ == "__main__":  # pragma: no cover
    from quo import print
    from quo.panel import Panel

    panel = Styled(Panel("hello"), "on blue")
    print(panel)
