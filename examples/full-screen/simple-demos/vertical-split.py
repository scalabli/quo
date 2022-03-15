#!/usr/bin/env python
"""
Vertical split example.
"""
from quo.console import Console
from quo.keys import Bind
from quo.layout import FormattedTextControl, Window, VSplit, Layout
from quo.text import Text

# 1. The layout
left_text = Text("""<b>Vertical-split  Press <red>'q'</red> to quit.

(left pane.)</b>""")
right_text = Text("""

        <b>(right pane)</b>""")


body = VSplit(
    [
        Window(FormattedTextControl(left_text)),
        Window(width=1, char="|", style="fg:green"),  # Vertical line in the middle.
        Window(FormattedTextControl(right_text)),
    ]
)


# 2. Key bindings
bind = Bind()

@bind.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`
Console(Layout(body), bind=bind, full_screen=True).run()
