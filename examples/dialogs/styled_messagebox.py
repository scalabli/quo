#!/usr/bin/env python
"""
Example of a style dialog window.
All dialog shortcuts take a `style` argument in order to apply a custom
styling.

This also demonstrates that the `title` argument can be any kind of formatted
text.
"""

from quo import MessageBox
from quo.text import Text
from quo.style import Style

# Custom color scheme.

example_style = Style.add(
    {
        "dialog": "bg:aquamarine",
        "dialog frame-label": "bg:purple",
        "dialog.body": "bg:#000000 #00ff00",
        "dialog shadow": "bg:yellow",
    }
)

MessageBox(
        title=Text(
            '<style bg="blue" fg="white">Styled</style> ' '<style fg="red">dialog</style> window'),
        text="Do you want to continue?\nPress ENTER to quit.", style=example_style).run()

