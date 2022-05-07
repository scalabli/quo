#!/usr/bin/env python
"""
Example of printing colored text to the output.
"""
import time
import multiprocessing
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
    def ok(text_fragments, style):
        return print(text_fragments, style=style)

    def oks(dits):
        with multiprocessing.Pool() as pool:
            pool.map(ok, dits)
    #print(text_fragments, style=style)

    # Print using an HTML object.
    print("<hello>hello</hello> <world>world</world>\n", style=style)

    # Print using an HTML object with inline styling.
    print('<style fg="#ff0066">hello</style> '
            '<style fg="#44ff44"><i>world</i></style>\n'
        )

if __name__ == "__main__":
    start = time.time()
    main()
    duration = time.time() - start
    print(f"Duration {duration}")
