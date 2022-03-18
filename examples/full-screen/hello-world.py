#!/usr/bin/env python
"""
A simple example of a a text area displaying "Hello World!".
"""

from quo import container
from quo.keys import Bind
from quo.widget import Box, Frame, TextArea

# Layout for displaying hello world.
# (The frame creates the border, the box takes care of the margin/padding.)

bind = Bind()

# The Key bindings
@bind.add("ctrl-c")
def _(event):
    "Quit when control-c is pressed."
    event.app.exit()


container(
        Box(
            Frame(
                TextArea("Hello world!\nPress control-c to quit.", width=40, height=10)
            )
        ),
        bind=bind,
        full=True,
        pre_run=True
        )

   
