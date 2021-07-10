import inspect
import io
import itertools
import os
import struct
import sys

from quo.accordance import DEFAULT_COLUMNS
from quo.accordance import get_winterm_size
from quo.accordance import is_bytes
from quo.accordance import isatty
from quo.accordance import strip_ansi_colors
from quo.accordance import WIN
from quo.outliers.exceptions import Abort
from quo.outliers.exceptions import UsageError
from quo.context.current import resolve_color_default
from quo.types import Choice
from quo.types import convert_type
from quo.output.inscribe import echo
#rom quo.expediency.utilities import echo
from quo.expediency.utilities import LazyFile

# The prompt functions to use.  The doc tools currently override these
# functions to customize how they work.
visible_prompt_func = input
#American National Standard Institute colors

ansi_color_codes = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "reset": 39,
    "vblack": 90,
    "vred": 91,
    "vgreen": 92,
    "vyellow": 93,
    "vblue": 94,
    "vmagenta": 95,
    "vcyan": 96,
    "vwhite": 97,
}
_ansi_reset_all = "\033[0m"


def hidden_prompt_func(prompt):
    import getpass

    return getpass.getpass(prompt)


def _build_prompt(
    text, suffix, show_default=False, default=None, show_choices=True, type=None
):
    prompt = text
    if type is not None and show_choices and isinstance(type, Choice):
        prompt += f" ({', '.join(map(str, type.choices))})"
    if default is not None and show_default:
        prompt = f"{prompt} [{_format_default(default)}]"
    return f"{prompt}{suffix}"


def _format_default(default):
    if isinstance(default, (io.IOBase, LazyFile)) and hasattr(default, "name"):
        return default.name

    return default

##################################################################
def prompt(
    text,
    default=None,
    hide=False,
    autoconfirm=False,
    type=None,
    value_proc=None,
    prompt_suffix=": ",
    show_default=True,
    err=False,
    show_choices=True,
):
    """Prompts a user for input.  This is a convenience function that can
    be used to prompt a user for input later.

    If the user aborts the input by sending a interrupt signal, this
    function will catch it and raise a :exc:`Abort` exception.

    :param text: the text to show for the prompt.
    :param default: the default value to use if no input happens.  If this
                    is not given it will prompt until it's aborted.
    :param hide_input: if this is set to true then the input value will
                       be hidden.
    :param autoconfirm: asks for confirmation for the value.
    :param type: the type to use to check the value against.
    :param value_proc: if this parameter is provided it's a function that
                       is invoked instead of the type conversion to
                       convert a value.
    :param prompt_suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of
                ``stdout``, the same as with echo.
    :param show_choices: Show or hide choices if the passed type is a Choice.
                         For example if type is a Choice of either day or week,
                         show_choices is true and text is "Group by" then the
                         prompt will be "Group by (day, week): ".
    """
    result = None

    def prompt_func(text):
        f = hidden_prompt_func if hide else visible_prompt_func
        try:
            # Write the prompt separately so that we get nice
            # coloring through colorama on Windows
            echo(text, nl=False, err=err)
            return f("")
        except (KeyboardInterrupt, EOFError):
            # Note:  getpass doesn't print a newline if the user aborts input with ^C.
            # Allegedly this behavior is inherited from getpass(3).
            # A doc bug has been filed at https://bugs.python.org/issue24711
            if hide:
                echo(None, err=False)
            raise Abort()

    if value_proc is None:
        value_proc = convert_type(type, default)

    prompt = _build_prompt(
        text, prompt_suffix, show_default, default, show_choices, type
    )

    while 1:
        while 1:
            value = prompt_func(prompt)
            if value:
                break
            elif default is not None:
                value = default
                break
        try:
            result = value_proc(value)
        except UsageError as e:
            if hide:
                flair("Error: the value you entered was invalid", err=err, fg="black", bg="yellow")
            else:
                echo(f"Error: {e.message}", err=err)  # noqa: B306
            continue
        if not autoconfirm:
            return result
        while 1:
            value2 = prompt_func("Repeat for confirmation: ")
            if value2:
                break
        if value == value2:
            return result
        flair("Error: the two entered values do not match", err=err, fg="black", bg="yellow")
###########################################################################
