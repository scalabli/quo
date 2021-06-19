"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from .core import Argument
from .core import BaseCommand
from .core import Command
from .core import CommandCollection
from .core import Context
from .core import Tether
from .core import MultiCommand
from .core import App
from .core import Parameter
from .core import ShellDetectionFailure
from quo.decorators.decorate import argument
from quo.decorators.decorate import command
from quo.decorators import autoconfirm
from quo.decorators.decorate import tether
from quo.decorators import autohelp
from quo.decorators.decorate import make_pass_decorator
from quo.decorators.decorate import app
from quo.decorators.decorate import contextualize
from quo.decorators.decorate import objectualize
from quo.decorators import autopswd
from quo.decorators import autoversion
from quo.outliers.exceptions import Abort
from quo.outliers.exceptions import BadArgumentUsage
from quo.outliers.exceptions import BadOptionUsage
from quo.outliers.exceptions import BadParameter
from quo.outliers.exceptions import QuoException
from quo.outliers.exceptions import FileError
from quo.outliers.exceptions import MissingParameter
from quo.outliers.exceptions import NoSuchOption
from quo.outliers.exceptions import UsageError
from .layout import HelpFormatter
from .layout import wraptext
from quo.context.current import currentcontext
from .parser import AppParser
from quo.ui.termui import clear
from quo.ui.termui import confirm
from quo.ui.termui import scrollable
from quo.ui.termui import edit
from quo.ui.termui import terminalsize
from quo.ui.termui import interpose 
from quo.ui.termui import launch
from quo.ui.termui import pause
from quo.ui.termui import progressbar
from quo.ui.termui import prompt
from quo.ui.termui import flair
from quo.ui.termui import style
from quo.ui.termui import unstyle
from .types import BOOL
from .types import Choice
from .types import DateTime
from .types import File
from .types import FLOAT
from .types import FloatRange
from .types import INT
from .types import IntRange
from .types import ParamType
from .types import Path
from .types import STRING
from .types import Tuple
from .types import UNPROCESSED
from .types import UUID
from quo.expediency.utilities import echo
from quo.expediency.utilities import formatfilename
from quo.expediency.utilities import get_app_dir
from quo.expediency.utilities import get_binary_stream
from quo.expediency.utilities import get_os_args
from quo.expediency.utilities import get_text_stream
from quo.expediency.utilities import openfile


__version__ = "2021.2"
