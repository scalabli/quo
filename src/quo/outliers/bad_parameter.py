from quo.accordance import filename_to_ui
from quo.accordance import get_text_stderr
from quo.utilities import echo

from typing import Any, Dict, Optional, Sequence, Type


class BadParameter(UsageError):
    """This exception formats out a standardized error message for a
    bad parameter.


    :param param: the parameter object that caused this error.  This can
                  be left out, and Quo will attach this info itself
                  if possible.
    :param param_hint: a string that shows up as parameter name.  This
                       can be used as alternative to `param` in cases
                       where custom validation should happen.  If it is
                       a string it's used as such, if it's a list then
                       each item is quoted and separated.
    """

    def __init__(self, message, ctx=None, param=None, param_hint=None):
        super().__init__(message, ctx)
        self.param = param
        self.param_hint = param_hint

    def format_message(self):
        if self.param_hint is not None:
            param_hint = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.ctx)
        else:
            return f"Invalid value: {self.message}"
        param_hint = _join_param_hints(param_hint)

        return f"Invalid value for {param_hint}: {self.message}"
