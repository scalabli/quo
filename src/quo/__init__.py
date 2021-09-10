"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from quo.i_o.termui import ansi_color_codes, _ansi_reset_all
from quo.outliers import Abort, UsageError
from quo.application import Application
from .core import (
             App,
             Arg,
             BaseCommand,
             Command,
             CommandCollection,
             Context,
             MultiCommand,
             Parameter,
             ShellDetectionFailure,
             Tether
             )



from quo.accordance import (
        DEFAULT_COLUMNS,
        get_winterm_size,
        strip_ansi_colors
        )

from quo.outliers import Abort, UsageError
from quo.context.current import resolve_color_default
from quo.types import Choice, convert_type
from quo.expediency import inscribe, LazyFile
from quo.outliers import Abort, UsageError
from quo.context.current import resolve_color_default
from quo.types import Choice, convert_type
from quo.expediency import inscribe, LazyFile

from quo.text import ANSI, HTML
from quo.output import ColorDepth
from quo.shortcuts import button_dialog
from quo.shortcuts import message_dialog
from quo.shortcuts.utils import print_formatted_text
from quo.indicators import ProgressBar
from quo.shortcuts import Elicit
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

from quo.outliers import (
                   Abort,
                   BadArgUsage,
                   BadAppUsage,
                   BadParameter,
                   QuoException,
                   FileError,
                   MissingParameter,
                   NoSuchApp,
                   UsageError
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
    import os
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
              checknumber,
              checkbool,
              checkinteger,
              confirm,
              launch,
              echo,
        #      interpose,
              edit,
              terminalsize,
           #   pause,
              style,
              unstyle,
             # prompt,
              )

from quo.shortcuts import container
from quo.widgets import TextArea, Frame
from quo.systematize import tabular
from .types import (
              BOOL,
              Choice,
              DateTime,
              File,
              FLOAT,
              FloatRange,
              INT,
              IntRange,
              ParamType,
              Path,
              STRING,
              Tuple,
              UNPROCESSED,
              UUID
              )

__version__ = "2021.5.5"
