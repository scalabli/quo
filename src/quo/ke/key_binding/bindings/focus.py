from quo.keys.key_binding.key_processor import KeyPressEvent

__all__ = [
    "next",
    "previous",
]

E = KeyPressEvent


def next(event: E) -> None:
    """
    Focus the next visible Window.
    (Often bound to the `Tab` key.)
    """
    event.app.layout.next()


def previous(event: E) -> None:
    """
    Focus the previous visible Window.
    (Often bound to the `BackTab` key.)
    """
    event.app.layout.previous()
