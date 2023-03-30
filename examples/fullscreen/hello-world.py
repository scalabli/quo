#!/usr/bin/env python
"""
A simple example of a a text area displaying "Hello World!".
"""

from quo import container
from quo.widget import Box, Frame, TextArea

# Layout for displaying hello world.
# (The frame creates the border, the box takes care of the margin/padding.)

container(
        Box(
            Frame(
                TextArea("Hello world!\nPress control-c to quit.")
            )
        ),
        bind=True,
        full_screen=True
        )

   
