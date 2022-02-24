#!/usr/bin/env python
"""
Simple example of a CLI that demonstrates up-arrow partial string matching.

When you type some input, it's possible to use the up arrow to filter the
history on the items starting with the given input text.
"""

from quo import print
from quo.prompt import Prompt
from quo.history import InMemoryHistory


def main():
    # Create some history first. (Easy for testing.)
    history = InMemoryHistory()
    history.append("import os")
    history.append('print("hello")')
    history.append('print("world")')
    history.append("import path")

    # Print help.
    print("This CLI has up-arrow partial string matching enabled.")
    print('Type for instance "pri" followed by up-arrow and you')
    print('get the last items starting with "pri".')
    print("Press Control-C to retry. Control-D to exit.")

    session = Prompt(history=history)

    while True:
        try:
            text = session.prompt("Say something: ")
        except KeyboardInterrupt:
            pass  # Ctrl-C pressed. Try again.
        else:
            break

    print(f"You said: {text}")


if __name__ == "__main__":
    main()
