#!/usr/bin/env python
"""
Colorcolumn example.
"""
from quo.buffer import Buffer
from quo.console import Console
from quo.keys import Bind
from quo.layout.containers import ColorColumn, HSplit, Window
from quo.layout.controls import BufferControl, FormattedTextControl
from quo.layout.layout import Layout

LIPSUM = """
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

# Create text buffers.
buff = Buffer()
buff.text = LIPSUM

# 1. The layout
color_columns = [
    ColorColumn(50),
    ColorColumn(80, style="bg:#ff0000"),
    ColorColumn(10, style="bg:#ff0000"),
]

console = Console()

body = HSplit(
    [
        Window(FormattedTextControl('Press "q" to quit.'), height=1, style="reverse"),
        Window(BufferControl(buffer=buff), colorcolumns=color_columns),
    ]
)


# 2. Key bindings
bind =  Bind()

@bind.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`
Console(layout=Layout(body), bind=bind, full_screen=True).run()
