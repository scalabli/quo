import sys
from typing import Optional, TextIO

from quo.utils.utils import is_windows

from .core import Input
from .core import PipeInput

__all__ = [
    "create_input",
    "create_pipe_input",
]


def create_input(
    stdin: Optional[TextIO] = None, always_prefer_tty: bool = False
) -> Input:
    """
    Create the appropriate `Input` object for the current os/environment.

    :param always_prefer_tty: When set, if `sys.stdin` is connected to a Unix
        `pipe`, check whether `sys.stdout` or `sys.stderr` are connected to a
        pseudo terminal. If so, open the tty for reading instead of reading for
        `sys.stdin`. (We can open `stdout` or `stderr` for reading, this is how
        a `$PAGER` works.)
    """
    if is_windows():
        from .win32 import Win32Input

        return Win32Input(stdin or sys.stdin)
    else:
        from .videoterminal import Vt100

        # If no input TextIO is given, use stdin/stdout.
        if stdin is None:
            stdin = sys.stdin

            if always_prefer_tty:
                for io in [sys.stdin, sys.stdout, sys.stderr]:
                    if io.isatty():
                        stdin = io
                        break

        return Vt100(stdin)


def create_pipe_input() -> PipeInput:
    """
    Create an input pipe.
    This is mostly useful for unit testing.
    """
    if is_windows():
        from .win32_pipe import Win32PipeInput

        return Win32PipeInput()
    else:
        from .posix_pipe import PosixPipeInput

        return PosixPipeInput()
