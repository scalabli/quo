"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""

import os
import sys

from .pause import pause as pause
from .prompt import (
    prompt as prompt,
)  # dont confuse this with :class: quo.prompt.Prompt()



def clear() -> None:

    """Clears the terminal screen and moves the cursor to the top left.
       :return: None
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    

def exit(code: int):

    """
    Exit the interpreter immediately using os._exit()

    This function provides a low-level exit that bypasses the normal Python
    shutdown process and immediately terminates the interpreter. This can
    be useful in situations where a faster exit is needed, such as shell
    completion or other interactive applications.

    Args:
        code (int, optional): The exit status code. Defaults to 0.

    Returns:
        None
    """
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)


def getchar(inscribe: bool = False):
    """Fetches a single character from the terminal and returns it.  This
    will always return a unicode character and under certain rare
    circumstances this might return more than one character.  The
    situations which more than one character is returned is when for
    whatever reason multiple characters end up in the terminal buffer or
    standard input was not actually a terminal.
    Note that this will always read from the terminal, even if something
    is piped into the standard input.
    Note for Windows: in rare cases when typing non-ASCII characters, this
    function might wait for a second character and then return both at once.
    This is because certain Unicode characters look like special-key markers.
    :param inscribe: if set to `True`, the character read will also show up on the terminal.  The default is to not show it.
    """
    from quo.expediency.vitals import inscribe

    _interpose = None
    f = _interpose
    if f is None:
        from quo.implementation import interpose as f
    return f(inscribe)



def print(
        *values, #: Any,
        end="\n ",
        include_default_pygments_style=None,
        sep=" ",
        style=None,
        output=None,
        colorDepth=None,
        style_transformation=None
        ) ->None:

    from quo.shortcuts.utils import _print
    from quo.text.html import Text
    _print(Text(*values), end=end, include_default_pygments_style=include_default_pygments_style, color_depth=colorDepth, style=style, output=output, sep=sep, style_transformation=style_transformation)
        
    

#from quo.shortcuts.utils import print
from quo.i_o.termui import confirm, echo
from quo.shortcuts.utils import container

__version__ = "2023.5"
