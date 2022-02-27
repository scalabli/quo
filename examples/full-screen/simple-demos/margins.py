#!/usr/bin/env python
"""
Example of Window margins.

This is mainly used for displaying line numbers and scroll bars, but it could
be used to display any other kind of information as well.
"""

from quo.buffer import Buffer
from quo.console import Console
from quo.keys import Bind
from quo.layout import HSplit, Layout, Window
from quo.layout import BufferControl, FormattedTextControl
from quo.layout.margin import NumberedMargin, ScrollbarMargin

LIPSUM = ( """Quo is scallable\n"""  * 40)

# Create text buffers. The margins will update if you scroll up or down.

buff = Buffer()
buff.text = LIPSUM

# 1. The layout
body = HSplit(
    [
        Window(FormattedTextControl('Press "q" to quit.'), height=1, style="fg:red bg:yellow bold"),
        Window(
            BufferControl(buffer=buff),
            # Add margins.
            left_margins=[NumberedMargin(), ScrollbarMargin()],
            right_margins=[ScrollbarMargin(), ScrollbarMargin()],
        ),
    ]
)


# 2. Key bindings
kb = Bind()

@kb.add("q")
@kb.add("ctrl-c")
def _(event):
    "Quit application."
    event.app.exit()

# Layout
layout = Layout(body)
# 3. The `Application`
application = Console(layout=layout, bind=kb)# full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
