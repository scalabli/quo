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
from .core import Option
from .core import Parameter
from .core import ShellDetectionFailure
from .decorators import argument
from .decorators import command
from .decorators import autoconfirm
from .decorators import tether
from .decorators import autohelp
from .decorators import make_pass_decorator
from .decorators import option
from .decorators import contextualize
from .decorators import objectualize
from .decorators import autopswd
from .decorators import autoversion
from .exceptions import Abort
from .exceptions import BadArgumentUsage
from .exceptions import BadOptionUsage
from .exceptions import BadParameter
from .exceptions import QuoException
from .exceptions import FileError
from .exceptions import MissingParameter
from .exceptions import NoSuchOption
from .exceptions import UsageError
from .layout import HelpFormatter
from .layout import wraptext
from quo.context.current import currentcontext
from .parser import OptionParser
from .termui import clear
from .termui import confirm
from .termui import scrollable
from .termui import edit
from .termui import terminalsize
from .termui import interpose 
from .termui import launch
from .termui import pause
from .termui import progressbar
from .termui import prompt
from .termui import flair
from .termui import style
from .termui import unstyle
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
from .utilities import echo
from .utilities import formatfilename
from .utilities import get_app_dir
from .utilities import get_binary_stream
from .utilities import get_os_args
from .utilities import get_text_stream
from .utilities import openfile



__version__ = "2021.5.dev11"
