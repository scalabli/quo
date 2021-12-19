#!/usr/bin/env python
"""
Vertical split example.
"""
import quo

from quo.layout.controls import FormattedTextControl

# 1. The layout
left_text = "\nVertical-split example. Press 'q' to quit.\n\n(left pane.)"
right_text = "\n(right pane.)"


body = quo.layout.VSplit(
    [
        quo.layout.Window(FormattedTextControl(left_text)),
        quo.layout.Window(width=1, char="|"),  # Vertical line in the middle.
        quo.layout.Window(FormattedTextControl(right_text)),
    ]
)


# 2. Key bindings
kb = quo.keys.KeyBinder()


@kb.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`
application = quo.Suite(layout=quo.layout.Layout(body), key_bindings=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
