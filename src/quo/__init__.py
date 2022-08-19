"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""

import os
import sys

# from .core import Clime as Clime
# from .core import Parameter as Parameter
# from .core import App as App
# from .core import Tether as Tether
from .pause import pause as pause
from .prompt import (
    prompt as prompt,
)  # dont confuse this with :class: quo.prompt.Prompt()


#             Arg,
#             BaseCommand,
#             Command,
#             CommandCollection,
#             MultiCommand,


# from quo.accordance import (
#        DEFAULT_COLUMNS,
#        get_winterm_size,
#        strip_ansi_colors
#        )

# from quo.context.current import resolve_color_default
# from quo.expediency import inscribe # LazyFile

# from quo.decorators import (
#             contextualize,
#             objectualize,
#             make_pass_decorator
#             autoversion,
#             autopasswd,
#             autohelp,
#             autoconfirm


# from .setout import HelpFormatter, wraptext
# from quo.context.current import currentcontext as pass_clime
# from .parser import AppParser

from quo.expediency.vitals import (
    appdir,
    formatfilename,
    os_args,
    textstream,
    binarystream,
)


def clear() -> None:
    from .accordance import isatty, WIN

    """Clears the terminal screen and moves the cursor to the top left.
    """
    if not isatty(sys.stdout):
        return

    if WIN:
        os.system("class")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


def exit(code: int):

    """Low-level exit that skips Python's cleanup but speeds up exit by about 10ms for things like shell completion.
    :param code: Exit code.
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
        fmt:bool= False,
        include_default_pygments_style=None,
        style=None,
        sep=" ",
        output=None,
        style_transformation=None
        ) ->None:

    from quo.shortcuts.utils import _print
    from quo.text.core import FormattedText
    from quo.text.html import Text
    if fmt:

        _print(
                FormattedText(
                    [
                        [*values]
                        ]
                    ),
                end=end,
                include_default_pygments_style=include_default_pygments_style,
                output=output, 
                sep=sep,
                style=style,
                style_transformation=style_transformation
                )
    else:
        _print(Text(*values), end=end, include_default_pygments_style=include_default_pygments_style, output=output, sep=sep, style=style, style_transformation=style_transformation)

#from quo.shortcuts.utils import print
from quo.i_o.termui import confirm, echo
from quo.shortcuts.utils import container

__version__ = "2022.8"
