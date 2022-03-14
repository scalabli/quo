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
            "dialog": "bg:aquamarine",
            "dialog.body": "bg:black fg:green",
            "dialog.shadow": "bg:yellow",
            }
        )

MessageBox(
        title=Text(
            '<style bg="blue" fg="white">Styled</style> ' '<style fg="red">dialog</style> window'),
        text="Do you want to continue?\nPress ENTER to quit.", 
        style=style)
