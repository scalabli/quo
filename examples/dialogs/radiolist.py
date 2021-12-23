#!/usr/bin/env python
"""
Example of a radio list box dialog.
"""

import quo

from quo.shortcuts import radiolist


def main():
    result = radiolist(
        values=[
            ("red", "Red"),
            ("green", "Green"),
            ("blue", "Blue"),
            ("orange", "Orange"),
        ],
        title="Radiolist dialog example",
        text="Please select a color:",
    ).run()

    print("Result = {}".format(result))

    # With HTML.
    result = radiolist(
        values=[
            ("red", quo.text.HTML('<style bg="red" fg="white">Red</style>')),
            ("green", quo.text.HTML('<style bg="green" fg="white">Green</style>')),
            ("blue", quo.text.HTML('<style bg="blue" fg="white">Blue</style>')),
            ("orange",quo.text.HTML('<style bg="orange" fg="white">Orange</style>')),
        ],
        title=quo.text.HTML("Radiolist dialog example <reverse>with colors</reverse>"),
        text="Please select a color:",
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
