"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from quo.application import Suite
from quo.types import Choice, convert_type
from quo.text import ANSI, HTML
from quo.align import Align
from quo.bar import Bar
from quo.columns import Columns
from quo.console import Console
from quo.console import Group
from quo.color.color import Color
from quo.layout import Outline
from quo.output import ColorDepth
from quo.pad import Padding
from quo.panel import Panel
from quo.shortcuts import Elicit
from quo.style import Style
from quo.table import Table
from quo.text import Text
from quo.pause import pause
#from quo.styles import Style
from quo.decorators import (
                       app,
                       arg,
                       command,
                       tether
                       )

from .parser import AppParser
from quo.expediency import (
                  inscribe,
                  appdir,
                  formatfilename,
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
              prompt,
              )

from quo.tabulate import tabular

import typing
OverflowMethod = typing.Literal["fold", "crop", "ellipsis", "ignore"]

__version__ = "2021.6.5"
