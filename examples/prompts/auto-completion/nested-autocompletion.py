#!/usr/bin/env python
"""
Example of nested autocompletion.
"""
import quo

session = quo.Prompt()


completer = quo.completion.NestedCompleter.add(
    {
        "show": {"version": None, "clock": None, "ip": {"interface": {"brief": None}}},
        "exit": None,
    }
)


def main():
    text = session.prompt("Type a command: ", completer=completer)
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
