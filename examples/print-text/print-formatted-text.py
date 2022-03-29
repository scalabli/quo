#!/usr/bin/env python
"""
Example of printing colored text to the output.
"""
from quo import print
from quo.text import FormattedText
from quo.style import Style

def main():
    style = Style.add(
        {
            "hello": "#ff0066",
            "world": "#44ff44 italic",
        }
    )

    # Print using a a list of text fragments.
    text_fragments = FormattedText(
        [
            ("class:hello", "Hello "),
            ("class:world", "World"),
            ("", "\n"),
        ]
    )
    print(text_fragments, style=style)

    # Print using an HTML object.
    print("<hello>hello</hello> <world>world</world>\n", style=style)

    # Print using an HTML object with inline styling.
    print('<style fg="#ff0066">hello</style> '
            '<style fg="#44ff44"><i>world</i></style>\n'
        )

if __name__ == "__main__":
    main()
