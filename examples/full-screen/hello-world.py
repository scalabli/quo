#!/usr/bin/env python
"""
A simple example of a a text area displaying "Hello World!".
"""

import quo

# Layout for displaying hello world.
# (The frame creates the border, the box takes care of the margin/padding.)
root_container = quo.widgets.Box(
    quo.widgets.Frame(
        quo.widgets.TextArea(
            text="Hello world!\nPress control-c to quit.",
            width=40,
            height=10,
        )
    ),
)
layout = quo.layout.Layout(container=root_container)


# Key bindings.
kb = quo.keys.KeyBinder()


@kb.add("ctrl-c")
def _(event):
    "Quit when control-c is pressed."
    event.app.exit()


# Build a main application object.
application = quo.Suite(layout=layout, key_bindings=kb, full_screen=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
