"""
Dummy layout. Used when somebody creates a `Console Application` without specifying a `Layout`.
"""
from quo.text.html import Text
from quo.keys import Bind

from .containers import Window
from .controls import FormattedTextControl
from .dimension import D
from .layout import Layout

__all__ = [
    "create_dummy_layout",
]


def create_dummy_layout() -> Layout:
    """
    Create a dummy layout for use in an 'Application' that doesn't have a
    layout specified. When ENTER is pressed, the application quits.
    """
    from quo.event import Event
    bind = Bind()

    @bind.add("enter")
    def enter(event: Event) -> None:
        event.app.exit()

    control = FormattedTextControl(
            Text("<b><red>»</red> <green>No layout was specified.</green></b> \nPress <reverse>ENTER</reverse> to quit.\n\n» <khaki>https://quo.rtfd.io</khaki>"),
            bind=bind,
    )
    window = Window(content=control, height=D(min=1))
    return Layout(container=window, focused_element=window)
