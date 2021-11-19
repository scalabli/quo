"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from quo.application import Suite
#from .core import (
#             App,
#             Arg,
#             BaseCommand,
#             Command,
#             CommandCollection,
#             Context,
#             MultiCommand,
#             Parameter,
#             Tether
#             )

from quo.types import Choice, convert_type
from quo.text import ANSI, HTML
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

#from quo.decorators import (
#             contextualize,
#             objectualize,
#             make_pass_decorator,
#             autoversion,
#             autopasswd,
#            autohelp,
#             autoconfirm
#             )

#from .setout import HelpFormatter, wraptext
#from quo.context.current import currentcontext
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

#from quo.shortcuts import container
#from quo.widget import TextArea, Frame



__version__ = "2021.6"
