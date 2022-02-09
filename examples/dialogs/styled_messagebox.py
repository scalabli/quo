#!/usr/bin/env python
"""
Example of a style dialog window.
All dialog shortcuts take a `style` argument in order to apply a custom
styling.

This also demonstrates that the `title` argument can be any kind of formatted
text.
"""

import quo


# Custom color scheme.

styling = quo.styles.Style

example_style = styling.add(
    {
        "dialog": "bg:aquamarine",
        "dialog frame-label": "bg:purple",
        "dialog.body": "bg:#000000 #00ff00",
        "dialog shadow": "bg:yellow",
    }
)


def main():
    quo.MessageBox(
            title=quo.text.HTML(
                '<style bg="blue" fg="white">Styled</style> ' '<style fg="red">dialog</style> window'  ),
        text="Do you want to continue?\nPress ENTER to quit.",
        style=example_style,
        ).run()


if __name__ == "__main__":
    main()
