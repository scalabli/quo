#!/usr/bin/env python
"""
Example of Window margins.

This is mainly used for displaying line numbers and scroll bars, but it could
be used to display any other kind of information as well.
"""

from quo import container
from quo.buffer import Buffer
from quo.layout import HSplit, Layout, Window
from quo.layout import BufferControl, FormattedTextControl
from quo.layout.margin import NumberedMargin, ScrollbarMargin
from quo.text import Text

LIPSUM = ("""Quo is scallable\n""") *30

# Create text buffers. The margins will update if you scroll up or down.

buff = Buffer()
buff.text = LIPSUM

# 1. The layout
content = HSplit(
    [
        Window(FormattedTextControl('Press "ctrl-c" to quit.'), height=1, style="fg:red bg:yellow bold"),
        Window(
            BufferControl(buffer=buff),
            # Add margins.
            left_margins=[NumberedMargin(), ScrollbarMargin()],
            right_margins=[ScrollbarMargin(), ScrollbarMargin()],
        ),
    ]
)


# 3. The `Application`
container(content, bind=True, full_screen=True)
