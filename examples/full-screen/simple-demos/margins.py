#!/usr/bin/env python
"""
Example of Window margins.

This is mainly used for displaying line numbers and scroll bars, but it could
be used to display any other kind of information as well.
"""
import quo

from quo.layout import BufferControl, FormattedTextControl
from quo.layout.margin import NumberedMargin, ScrollbarMargin

LIPSUM = ( """Quo is scallable\n"""  * 40)

# Create text buffers. The margins will update if you scroll up or down.

buff = quo.buffer.Buffer()
buff.text = LIPSUM

# 1. The layout
hsplit = quo.layout.HSplit
window = quo.layout.Window
body = hsplit(
    [
        window(FormattedTextControl('Press "q" to quit.'), height=1, style="reverse"),
        window(
            BufferControl(buffer=buff),
            # Add margins.
            left_margins=[NumberedMargin(), ScrollbarMargin()],
            right_margins=[ScrollbarMargin(), ScrollbarMargin()],
        ),
    ]
)


# 2. Key bindings
kb = quo.keys.KeyBinder()

@kb.add("q")
@kb.add("ctrl-c")
def _(event):
    "Quit application."
    event.app.exit()

# Layout
layout = quo.layout.Layout
# 3. The `Application`
application = quo.Console(layout=layout(body), bind=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
