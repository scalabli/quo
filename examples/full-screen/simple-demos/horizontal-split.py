#!/usr/bin/env python
"""
Horizontal split example.
"""
from quo.console import Console
from quo.keys import Bind
from quo.layout import HSplit, Window, Layout, FormattedTextControl
# 1. The layout
left_text = "\nVertical-split example. Press 'q' to quit.\n\n(top pane.)"
right_text = "\n(bottom pane.)"


body = HSplit(
    [
        Window(FormattedTextControl(left_text)),
        Window(height=1, char="-"),  # Horizontal line in the middle.
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
application = Console(layout=Layout(body), bind=bind,full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
