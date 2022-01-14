#!/usr/bin/env python
"""
Example of an input box dialog.
"""

import quo

from quo.shortcuts import evoke


def main():
    result = evoke(
        title="Input dialog example", text="Please type your name:"
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
