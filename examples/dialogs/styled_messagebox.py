#!/usr/bin/env python
"""
Example of a style dialog window.
All dialog shortcuts take a `style` argument in order to apply a custom
styling.

This also demonstrates that the `title` argument can be any kind of formatted
text.
"""

from quo.dialog import MessageBox
from quo.text import Text
from quo.style import Style

# Custom color scheme.

style = Style.add(
        {
            "dialog": "bg:brown",
            "dialog.body": "bg:white fg:black",
            "dialog body.text-area": "fg:white bg:purple",
            "dialog frame.label": "fg:blue bg:green",
          #  "dialog.shadow": "bg:yellow",
            }
        )

MessageBox(
        title="fffff",
        #"Text(
        #    '<style bg="blue" fg="white">Styled</style> ' '<style fg="red">dialog</style> window')",
        text="Do you want to continue?\nPress ENTER to quit.", 
        style=style)
