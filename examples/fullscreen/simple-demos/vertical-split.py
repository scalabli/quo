#!/usr/bin/env python
"""
Vertical split example.
"""
from quo import container
from quo.layout import FormattedTextControl, Window, VSplit
from quo.text import Text

# 1. The layout
left_text = Text("""<b>Vertical-split  Press <red>'q'</red> to quit.

(left pane.)</b>""")
right_text = Text("""

        <b>(right pane)</b>""")

class dd:
    def __init__(self) -> None:

            Window(FormattedTextControl(left_text)),

        
        
content = VSplit([
    dd(),
    Window(width=1, char="|", style="fg:green"),  # Vertical line in the middle.
    Window(FormattedTextControl(right_text))
    ])


container(content, bind=True, full_screen=True)


