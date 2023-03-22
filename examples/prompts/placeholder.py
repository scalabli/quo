#!/usr/bin/env python3
"""
Example of a placeholer that's displayed as long as no input is given.
"""
from quo import echo
from quo.prompt import Prompt
from quo.text import Text

session = Prompt(placeholder=Text('<style fg="gray">(please type something)</style>'))

if __name__ == "__main__":
    answer = session.prompt(">> ")
    echo(f"You said: {answer}")
