from typing import Optional, Iterable, Union, Callable, Any
from abc import ABCMeta, abstractmethod
from quo.widget.core import Frame
from quo.layout.containers import Window
from quo.layout.controls import FormattedTextControl

from quo.utils.utils import get_width as get_cwidth

from quo.layout.dimension import AnyDimension

from quo.layout.dimension import Dimension as D
from quo.text.core import (
    AnyFormattedText as TextBlockRichText,
    to_formatted_text,
)
from quo.text.utils import fragment_list_to_text
from quo.history import History
from quo.keys.key_binding.key_bindings import Bind
from quo.layout.containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    DynamicContainer,
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
)



class TextBlock:
    """
    Widget that displays the given text. It is not editable or focusable.

    :param text: Text to display. Can be multiline. All value types accepted by
        :class:`quo.layout.FormattedTextControl` are allowed,
        including a callable.
    :param style: A style string.
    :param width: When given, use this width, rather than calculating it from
        the text size.
    :param dont_extend_width: When `True`, don't take up more width than
                              preferred, i.e. the length of the longest line of
                              the text, or value of `width` parameter, if
                              given. `True` by default
    :param dont_extend_height: When `True`, don't take up more width than the
                               preferred height, i.e. the number of lines of
                               the text. `False` by default.
    """

    def __init__(
        self,
        text: TextBlockRichText=None,
        style: str = "",
        frame:str="",
        align:str="center"
        ) -> None:
        from quo.layout.controls import FormattedTextControl


        if text is not None:
            self.text = FormattedTextControl(text)
        self.align=align

       
        if frame == "":
            
            def __pt_container__(self) -> Container:
                window = Window(content=text,align=align)

                return window
       


    


