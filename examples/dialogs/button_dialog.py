#!/usr/bin/env python
"""
Example of button dialog window.
"""

import quo

from quo.shortcuts import button

def main():
    result = button(
        title="Button dialog example",
        text="Are you sure?",
        buttons=[("Yes", True), ("No", False), ("Maybe...", None)],
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
