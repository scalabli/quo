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
from .decorate import argument
from .decorate import command
from quo.decorators import autoconfirm
from .decorate import tether
from quo.decorators import autohelp
from .decorate import make_pass_decorator
from .decorate import option
from .decorate import contextualize
from .decorate import objectualize
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
from quo.expediency.utilities import echo
from quo.expediency.utilities import formatfilename
from quo.expediency.utilities import get_app_dir
from quo.expediency.utilities import get_binary_stream
from qou.expediency.utilities import get_os_args
from quo.expediency.utilities import get_text_stream
from quo.expediency.utilities import openfile



__version__ = "2021.6.dev1"
