#!/usr/bin/env python
"""
Example of nested autocompletion.
"""
from quo.completion import NestedCompleter
from quo.prompt import Prompt

completer = NestedCompleter.add(
        {
        "show": 
        {
            "version": None,
            "clock": None, 
            "ip": 
            {
                "interface": 
                {
                    "brief": None
                    }
                }
            },
        "exit": None,
    }
)

session = Prompt(completer=completer)

def main():
    text = session.prompt("Type a command: ", completer=completer)
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
