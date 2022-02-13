#!/usr/bin/env python
"""
A simple example of a a text area displaying "Hello World!".
"""

from quo import container
from quo import Console
from quo.keys import KeyBinder
from quo.layout import Layout
from quo.widgets import Box, Frame, TextArea

# Layout for displaying hello world.
# (The frame creates the border, the box takes care of the margin/padding.)
root_container = Box(
        Frame(
            TextArea(
                text="Hello world!\nPress control-c to quit.",
                width=40,
                height=10,
                )
            ),
        )
layout = Layout(container=root_container)


# Key bindings.
kb = KeyBinder()


@kb.add("ctrl-c")
def _(event):
    "Quit when control-c is pressed."
    event.app.exit()


# Build a main application object.
application = Console(
        layout=layout,
        bind=kb, 
        full_screen=True
        )


def main():
    application.run()


if __name__ == "__main__":
    main()
