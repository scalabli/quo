"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from typing import IO, TYPE_CHECKING, Any, Optional
from quo.application import Suite
from .core import (
             App,
             Arg,
             BaseCommand,
             Command,
             CommandCollection,
             Context,
             MultiCommand,
             Parameter,
             Tether
             )

from quo.types import Choice, convert_type
from quo.text import ANSI, HTML
from quo.align import Align
from quo.bar import Bar
from quo.console import Console
from quo.color.color import Color
from quo.output import ColorDepth
from quo.shortcuts import Elicit
from quo.pause import pause
from quo.styles import Style
from quo.decorators import (
                       app,
                       arg,
                       command,
                       tether
                       )

from quo.decorators import (
             contextualize,
             objectualize,
             make_pass_decorator,
             autoversion,
             autopasswd,
             autohelp,
             autoconfirm
             )

from .setout import HelpFormatter, wraptext
from quo.context.current import currentcontext
from .parser import AppParser
from quo.expediency import (
                  inscribe,
                  appdir,
                  formatfilename,
                  os_args,
                  textstream,
                  binarystream,
                  openfile
                  )
        

def clear():
    import sys
    from .accordance import isatty, WIN
    """Clears the terminal screen.  This will have the effect of clearing
    the whole visible space of the terminal and moving the cursor to the
    top left.  This does not do anything if not connected to a terminal.

    """
    if not isatty(sys.stdout):
        return

    if WIN:
        os.system("class")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


from quo.i_o import (
              confirm,
              launch,
              echo,
              edit,
              terminalsize,
              unstyle,
              prompt,
              )

from quo.shortcuts import container
from quo.widget import TextArea, Frame
from ._extension import load_ipython_extension

__all__ = ["get_console", "reconfigure", "inspect"]

if TYPE_CHECKING:
    from quo.console import Console

# Global console used by alternative print
_console: Optional["Console"] = None

_IMPORT_CWD = os.path.abspath(os.getcwd())


def get_console() -> "Console":
    """Get a global :class:`~quo.console.Console` instance. This function is used when Rich requires a Console,
    and hasn't been explicitly given one.

    Returns:
        Console: A console instance.
    """
    global _console
    if _console is None:
        from quo.console import Console

        _console = Console()

    return _console


def reconfigure(*args: Any, **kwargs: Any) -> None:
    """Reconfigures the global console by replacing it with another.

    Args:
        console (Console): Replacement console instance.
    """
    from quo.console import Console

    new_console = Console(*args, **kwargs)
    _console = get_console()
    _console.__dict__ = new_console.__dict__



def print_json(
    json: Optional[str] = None,
    *,
    data: Any = None,
    indent: int = 2,
    highlight: bool = True,
) -> None:
    """Pretty prints JSON. Output will be valid JSON.

    Args:
        json (str): A string containing JSON.
        data (Any): If json is not supplied, then encode this data.
        indent (int, optional): Number of spaces to indent. Defaults to 2.
        highlight (bool, optional): Enable highlighting of output: Defaults to True.
    """

    get_console().print_json(json, data=data, indent=indent, highlight=highlight)


def inspect(
    obj: Any,
    *,
    console: Optional["Console"] = None,
    title: Optional[str] = None,
    help: bool = False,
    methods: bool = False,
    docs: bool = True,
    private: bool = False,
    dunder: bool = False,
    sort: bool = True,
    all: bool = False,
    value: bool = True,
) -> None:
    """Inspect any Python object.

    * inspect(<OBJECT>) to see summarized info.
    * inspect(<OBJECT>, methods=True) to see methods.
    * inspect(<OBJECT>, help=True) to see full (non-abbreviated) help.
    * inspect(<OBJECT>, private=True) to see private attributes (single underscore).
    * inspect(<OBJECT>, dunder=True) to see attributes beginning with double underscore.
    * inspect(<OBJECT>, all=True) to see all attributes.

    Args:
        obj (Any): An object to inspect.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (beginning with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional): Sort attributes alphabetically. Defaults to True.
        all (bool, optional): Show all attributes. Defaults to False.
        value (bool, optional): Pretty print value. Defaults to True.
    """
    _console = console or get_console()
    from quo._inspect import Inspect

    # Special case for inspect(inspect)
    is_inspect = obj is inspect

    _inspect = Inspect(
        obj,
        title=title,
        help=is_inspect or help,
        methods=is_inspect or methods,
        docs=is_inspect or docs,
        private=private,
        dunder=dunder,
        sort=sort,
        all=all,
        value=value,
    )
    _console.print(_inspect)




__version__ = "2021.6"
