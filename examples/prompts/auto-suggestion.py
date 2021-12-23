#!/usr/bin/env python
"""
Simple example of a CLI that demonstrates fish-style auto suggestion.

When you type some input, it will match the input against the history. If One
entry of the history starts with the given input, then it will show the
remaining part as a suggestion. Pressing the right arrow will insert this
suggestion.
"""
import quo

from quo.auto_suggest import AutoSuggestFromHistory


def main():
    # Create some history first. (Easy for testing.)
    history = quo.history.InMemoryHistory()
    history.append_string("import os")
    history.append_string('print("hello")')
    history.append_string('print("world")')
    history.append_string("import path")

    # Print help.
    print("This CLI has fish-style auto-suggestion enable.")
    print('Type for instance "pri", then you\'ll see a suggestion.')
    print("Press the right arrow to insert the suggestion.")
    print("Press Control-C to retry. Control-D to exit.")
    print()

    session = quo.Prompt(
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
    )

    while True:
        try:
            text = session.prompt("Type something: ")
        except KeyboardInterrupt:
            pass  # Ctrl-C pressed. Try again.
        else:
            break

    quo.echo(f"You said: {text}")


if __name__ == "__main__":
    main()
