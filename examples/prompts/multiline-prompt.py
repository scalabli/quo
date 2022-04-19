#!/usr/bin/env python
"""
Demonstration of how the input can be indented.
"""
from quo.prompt import Prompt

session = Prompt(multiline=True)
if __name__ == "__main__":
    answer = session.prompt(
        "Give me some input: (ESCAPE followed by ENTER to accept)\n > ")
 #   echo(f"You said: {answer}")
