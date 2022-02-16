"""
Dummy layout. Used when somebody creates a `Console Application` without specifying a `Layout`.
"""
from quo.text import Text
from quo.keys import KeyBinder
from quo.keys.key_binding.key_processor import KeyPressEvent

from .containers import Window
from .controls import FormattedTextControl
from .dimension import D
from .layout import Layout

__all__ = [
    "create_dummy_layout",
]

E = KeyPressEvent


def create_dummy_layout() -> Layout:
    """
    Create a dummy layout for use in an 'Application' that doesn't have a
    layout specified. When ENTER is pressed, the application quits.
    """
    kb = KeyBinder()

    @kb.add("enter")
    def enter(event: E) -> None:
        event.app.exit()

    control = FormattedTextControl(
            Text("<i><green>🚫 No layout was specified.</green></i> \nPress <reverse>ENTER</reverse> to quit."),
        bind=kb,
    )
    window = Window(content=control, height=D(min=1))
    return Layout(container=window, focused_element=window)
