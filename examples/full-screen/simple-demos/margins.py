#!/usr/bin/env python
"""
Example of Window margins.

This is mainly used for displaying line numbers and scroll bars, but it could
be used to display any other kind of information as well.
"""
import quo

from quo.layout.controls import BufferControl, FormattedTextControl
from quo.layout.margins import NumberedMargin, ScrollbarMargin

LIPSUM = (
    """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Maecenas
quis interdum enim. Nam viverra, mauris et blandit malesuada, ante est bibendum
mauris, ac dignissim dui tellus quis ligula. Aenean condimentum leo at
dignissim placerat. In vel dictum ex, vulputate accumsan mi. Donec ut quam
placerat massa tempor elementum. Sed tristique mauris ac suscipit euismod. Ut
tempus vehicula augue non venenatis. Mauris aliquam velit turpis, nec congue
risus aliquam sit amet. Pellentesque blandit scelerisque felis, faucibus
consequat ante. Curabitur tempor tortor a imperdiet tincidunt. Nam sed justo
sit amet odio bibendum congue. Quisque varius ligula nec ligula gravida, sed
convallis augue faucibus. Nunc ornare pharetra bibendum. Praesent blandit ex
quis sodales maximus."""
    * 40
)

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
application = quo.Suite(layout=layout(body), bind=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
