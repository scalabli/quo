#!/usr/bin/env python
"""
Example of button dialog window.
"""
from quo import app, echo, command
from quo.shortcuts import button_dialog

@command()
@app("--button", help="Button dialog")
def main(button):
    result = button_dialog(
        title="Button dialog example",
        text="Are you sure?",
        buttons=[("Yes", True), ("No", False), ("Maybe...", None)],
    ).run()

    echo("Result = {}".format(result))


if __name__ == "__main__":
    main()
