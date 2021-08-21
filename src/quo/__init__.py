"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
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
        

from quo.i_o import (
              checknumber,
              checkbool,
              checkinteger,
              echo,
              confirm,
              launch,
              interpose,
              edit,
              terminalsize,
              pause,
              style,
              unstyle,
              prompt,
              clear
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

__version__ = "2021.4.5"
