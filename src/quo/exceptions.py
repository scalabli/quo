#
#
#
from .accordance import filename_to_ui
from .accordance import get_text_stderr
from .utilities import echo

from typing import Any, Dict, Optional, Sequence, Type



def _join_param_hints(param_hint):
    if isinstance(param_hint, (tuple, list)):
        return " / ".join(repr(x) for x in param_hint)
    return param_hint


class QuoException(Exception):
    """An exception that Quo can handle and show to the user."""

    #: The exit code for this exception.
    exit_code = 1

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def format_message(self):
        return self.message

    def __str__(self):
        return self.message

    def show(self, file=None):
        if file is None:
            file = get_text_stderr()
        echo(f"Error: {self.format_message()}", file=file)










class NoSuchOption(UsageError):
    """Raised if Quo attempted to handle an option that does not
    exist.

    """

    def __init__(self, option_name, message=None, possibilities=None, ctx=None):
        if message is None:
            message = f"no such option: {option_name}"

        super().__init__(message, ctx)
        self.option_name = option_name
        self.possibilities = possibilities

    def format_message(self):
        bits = [self.message]
        if self.possibilities:
            if len(self.possibilities) == 1:
                bits.append(f"Did you mean {self.possibilities[0]}?")
            else:
                possibilities = sorted(self.possibilities)
                bits.append(f"(Possible options: {', '.join(possibilities)})")
        return "  ".join(bits)


class BadOptionUsage(UsageError):
    """Raised if an option is generally supplied but the use of the option
    was incorrect.  This is for instance raised if the number of arguments
    for an option is not correct.

    :param option_name: the name of the option being used incorrectly.
    """

    def __init__(self, option_name, message, ctx=None):
        super().__init__(message, ctx)
        self.option_name = option_name


class BadArgumentUsage(UsageError):
    """Raised if an argument is generally supplied but the use of the argument
    was incorrect.  This is for instance raised if the number of values
    for an argument is not correct.

    """




class Abort(RuntimeError):
    """An internal signalling exception that signals Quo to abort."""


class Exit(RuntimeError):
    """An exception that indicates that the application should exit with some
    status code.

    :param code: the status code to exit with.
    """

    __slots__ = ("exit_code",)

    def __init__(self, code=0):
        self.exit_code = code
