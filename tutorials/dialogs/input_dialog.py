#!/usr/bin/env python
"""
Example of an input box dialog.
"""
from quo import echo, command, app
from quo.buttons import evoke

@command()
@app("--dialog", help="An example of an input dialog")
def main(dialog):
    result = evoke(
            title="Input dialog example",
            text="Please type your name:"
            ).run()
    echo("Result = {}".format(result))


if __name__ == "__main__":
    main()
