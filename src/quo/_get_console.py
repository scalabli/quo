from typing import Optional
from quo.console import Console

_console: Optional["Console"] = None

def _get_console() -> "Console":
    """Get a global :class:`~quo.console.Console` instance. This function is used when Quo requires a Console,
    and hasn't been explicitly given one.

    Returns:
        Console: A console instance.
    """
    global _console
    if _console is None:

        _console = Console()

    return _console
