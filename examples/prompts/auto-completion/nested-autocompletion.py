#!/usr/bin/env python
"""
Example of nested autocompletion.
"""
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import PromptSession as Prompt

completer = NestedCompleter.from_nested_dict(
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
