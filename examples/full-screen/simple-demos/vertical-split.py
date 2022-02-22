#!/usr/bin/env python
"""
Vertical split example.
"""
from quo.console import Console
from quo.layout import FormattedTextControl, Window, VSplit, Layout
from quo.keys import KeyBinder

# 1. The layout
left_text = "\nVertical-split example. Press 'q' to quit.\n\n(left pane.)"
right_text = "\n(right pane.)"


body = VSplit(
    [
        Window(FormattedTextControl(left_text)),
        Window(width=1, char="|"),  # Vertical line in the middle.
        Window(FormattedTextControl(right_text)),
    ]
)


# 2. Key bindings
kb = KeyBinder()


@kb.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`
Console(Layout(body), bind=kb, full_screen=True).run()

