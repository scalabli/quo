from quo.accordance import filename_to_ui
from quo.accordance import get_text_stderr
from quo.utilities import echo
from quo import exceptions

from typing import Any, Dict, Optional, Sequence, Type




class UsageError(QuoException):
    """An internal exception that signals a usage error.  This typically
    aborts any further handling.

    :param message: the error message to display.
    :param ctx: optionally the context that caused this error.  Quo will
                fill in the context automatically in some situations.
    """

    exit_code = 2

    def __init__(self, message, ctx=None):
        super().__init__(message)
        self.ctx = ctx
        self.cmd = self.ctx.command if self.ctx else None

    def show(self, file=None):
        if file is None:
            file = get_text_stderr()
        color = None
        hint = ""
        if self.cmd is not None and self.cmd.get_autohelp(self.ctx) is not None:
            hint = (
                f"Try '{self.ctx.command_path}"
                f" {self.ctx.autohelp_names[0]}' for help.\n"
            )
        if self.ctx is not None:
            color = self.ctx.color
            echo(f"{self.ctx.get_usage()}\n{hint}", file=file, color=color)
        echo(f"Error: {self.format_message()}", file=file, color=color)
