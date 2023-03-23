#!/usr/bin/env python3
"""
Example of a placeholer that's displayed as long as no input is given.
"""
from quo import echo
from quo.prompt import Prompt

session = Prompt()

answer = session.prompt(">> ", placeholder="<gray>(please type something)</gray>")

echo(f"You said: {answer}")
