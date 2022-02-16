"""
Many places in quo can take either plain text, or formatted text.
For instance the :class:`~quo.prompt.Pompt` function takes either
plain text or formatted text for the prompt. The
:class:`~quo.layout.FormattedTextControl` can also take either plain text or formatted text.

In any case, there is an input that can either be just plain text (a string),
an :class:`.HTML` object, an :class:`.ANSI` object or a sequence of
`(style_string, text)` tuples. The :func:`.to_formatted_text` conversion
function takes any of these and turns all of them into such a tuple sequence.
"""
from quo.i_o.output.html import Text
from quo.i_o.output.ansi import ANSI
from .core import (
    AnyFormattedText,
    FormattedText,
    StyleAndTextTuples,
    Template,
    is_formatted_text,
    merge_formatted_text,
    to_formatted_text,
)

from .pygments import PygmentsTokens
from .utils import (
    fragment_list_len,
    fragment_list_to_text,
    fragment_list_width,
    split_lines,
)

__all__ = [
    # Core
    "AnyFormattedText",
    "to_formatted_text",
    "is_formatted_text",
    "Text"
    "Template",
    "merge_formatted_text",
    "FormattedText",
    "StyleAndTextTuples",
    # HTML.
    "HTML",
    # ANSI.
    "ANSI",
    # Pygments.
    "PygmentsTokens",
    # Utils.
    "fragment_list_len",
    "fragment_list_width",
    "fragment_list_to_text",
    "split_lines",
]
