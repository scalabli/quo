import inspect
import io
import itertools
import os
import struct
import sys

from quo.accordance import DEFAULT_COLUMNS
from quo.accordance import get_winterm_size
from quo.accordance import is_bytes
from quo.accordance import isatty
from quo.accordance import strip_ansi_colors
from quo.accordance import WIN
from quo.outliers.exceptions import Abort
from quo.outliers.exceptions import UsageError
from quo.context.current import resolve_color_default
from quo.types import Choice
from quo.types import convert_type
from .inscribe  import echo
from quo.expediency.utilities import LazyFile



def pager(generated_text, color=None):
    """This function takes a text and shows it via an environment specific
    pager on stdout.

    :param generated_text: the text to page, or alternatively, a generator emitting the text to page.
    :param color: controls if the pager supports ANSI colors or not.  The default is autodetection.
    """
    color = resolve_color_default(color)

    if inspect.isgeneratorfunction(generated_text):
        i = generated_text()
    elif isinstance(generated_text, str):
        i = [generated_text]
    else:
        i = iter(generated_text)

    # convert every element of i to a text type if necessary
    text_generator = (el if isinstance(el, str) else str(el) for el in i)

    from quo.implementation import scrollable

    return pager(itertools.chain(text_generator, "\n"), color)
