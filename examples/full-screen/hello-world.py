#!/usr/bin/env python
"""
A simple example of a a text area displaying "Hello World!".
"""

from quo import container
from quo.console import Console
from quo.keys import Bind
from quo.layout import Layout
from quo.widget import Box, Frame, TextArea

# Layout for displaying hello world.
# (The frame creates the border, the box takes care of the margin/padding.)
root_container = Box(
        Frame(
            TextArea("Hello world!\nPress control-c to quit.",
                width=40,
                height=10,
                )
            ),
        )
layout = Layout(root_container)


# Key bindings.
bind = Bind()
console = Console()

@bind.add("ctrl-c")
def _(event):
    "Quit when control-c is pressed."
    event.app.exit()


# Build a main application object.
console(
        layout=layout,
        bind=bind, 
        full_screen=True
        ).run()
