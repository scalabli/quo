from .accordance import filename_to_ui
from .accordance import get_text_stderr
from .utilities import echo

from typing import Any, Dict, Optional, Sequence, Type





class MissingParameter(BadParameter):
    """This parameter is raised if Quo required an option or argument but it was not
    provided.

    :param param_type: a string that indicates the type of the parameter.
                       The default is to inherit the parameter type from
                       the given `param`.  Valid values are ``'parameter'``,
                       ``'option'`` or ``'argument'``.
    """

    def __init__(
        self, message=None, ctx=None, param=None, param_hint=None, param_type=None
    ):
        super().__init__(message, ctx, param, param_hint)
        self.param_type = param_type

    def format_message(self):
        if self.param_hint is not None:
            param_hint = self.param_hint
        elif self.param is not None:
            param_hint = self.param.get_error_hint(self.ctx)
        else:
            param_hint = None
        param_hint = _join_param_hints(param_hint)

        param_type = self.param_type
        if param_type is None and self.param is not None:
            param_type = self.param.param_type_name

        msg = self.message
        if self.param is not None:
            msg_extra = self.param.type.get_missing_message(self.param)
            if msg_extra:
                if msg:
                    msg += f".  {msg_extra}"
                else:
                    msg = msg_extra

        hint_str = f" {param_hint}" if param_hint else ""
        return f"Missing {param_type}{hint_str}.{' ' if msg else ''}{msg or ''}"

    def __str__(self):
        if self.message is None:
            param_name = self.param.name if self.param else None
            return f"missing parameter: {param_name}"
        else:
            return self.message
