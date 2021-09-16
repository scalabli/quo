#!/usr/bin/env python
"""
Example of a message box window.
"""
from quo import command, app
from quo.buttons import message

@command()
@app("--dialog", help="A message Dialog")
def main():
    message(
            title="Example dialog window"
            text="Do you want to continue?\nPress ENTER to quit.",
            ).run()


if __name__ == "__main__":
    main()
