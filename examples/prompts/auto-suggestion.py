#!/usr/bin/env python
"""
Simple example of a CLI that demonstrates fish-style auto suggestion.

When you type some input, it will match the input against the history. If One
entry of the history starts with the given input, then it will show the
remaining part as a suggestion. Pressing the right arrow will insert this
suggestion.
"""

from quo.history import MemoryHistory
from quo.prompt import Prompt

def main():
    # Create some history first. (Easy for testing.)
    MemoryHistory.append("import os")
    MemoryHistory.append('print("hello")')
    MemoryHistory.append('print("world")')
    MemoryHistory.append("import path")

    # Print help.
    print("This CLI has fish-style auto-suggestion enable.")
    print('Type for instance "pri", then you\'ll see a suggestion.')
    print("Press the right arrow to insert the suggestion.")
    print("Press Control-C to retry. Control-D to exit.")
    print()

    session = Prompt(
            history=MemoryHistory,
            suggest="history"
            )
      # auto_suggest=AutoSuggestFromHistory()
        #)

    while True:
        try:
            text = session.prompt("Type something:» ")
        except KeyboardInterrupt:
            pass  # Ctrl-C pressed. Try again.
        else:
            break

    print(f"You said: {text}")


if __name__ == "__main__":
    main()
