import sys
import typing

from quo.utils.utils import (
    get_bell_environment_variable,
    get_term_environment_variable,
    is_conemu_ansi,
    is_windows,
)

from .core import Output
from .color import ColorDepth

__all__ = [
    "create_output",
]


def create_output(
    stdout: typing.Optional[typing.TextIO] = None, always_prefer_tty: bool = True
) -> Output:
    """
    Return an :class:`~quo.output.Output` instance for the command
    line.

    :param stdout: The stdout object
    :param always_prefer_tty: When set, look for `sys.stderr` if `sys.stdout`
        is not a TTY. (The quo render output is not meant to be
        consumed by something other then a terminal, so this is a reasonable
        default.)
    """
    # Consider TERM, QUO_BELL, and QUO_COLOR_DEPTH
    # environment variables. Notice that QUO_COLOR_DEPTH value is
    # the default that's used if the Application doesn't override it.
    term_from_env = get_term_environment_variable()
    bell_from_env = get_bell_environment_variable()
    color_depth_from_env = ColorDepth.from_env()

    if stdout is None:
        # By default, render to stdout. If the output is piped somewhere else,
        # render to stderr.
        stdout = sys.stdout

        if always_prefer_tty:
            for io in [sys.stdout, sys.stderr]:
                if io.isatty():
                    stdout = io
                    break

    # If the patch_stdout context manager has been used, then sys.stdout is
    # replaced by this proxy. For quo applications, we want to use
    # the real stdout.
    from quo.patch_stdout import StdoutProxy

    while isinstance(stdout, StdoutProxy):
        stdout = stdout.original_stdout

    if is_windows():
        from .console_emulator import ConEmu
        from .win32 import Win32Output
        from .windows10 import Windows10_Output, is_win_vt100_enabled

        if is_win_vt100_enabled():
            return typing.cast(
                Output,
                Windows10_Output(stdout, default_color_depth=color_depth_from_env),
            )
        if is_conemu_ansi():
            return typing.cast(
                Output, ConEmu(stdout, default_color_depth=color_depth_from_env)
            )
        else:
            return Win32Output(stdout, default_color_depth=color_depth_from_env)
    else:
        from .videoterminal import Vt100

        return Vt100.from_pty(
            stdout,
            term=term_from_env,
            default_color_depth=color_depth_from_env,
            enable_bell=bell_from_env,
        )
