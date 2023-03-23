#!/usr/bin/env python3
"""
Example of a right prompt. This is an additional prompt that is displayed on
the right side of the terminal. It will be hidden automatically when the input
is long enough to cover the right side of the terminal.

This is similar to RPROMPT is Zsh.
"""
from quo import echo
from quo.prompt import Prompt


# Option 1: pass a brown colored  and italicized string 'rprompt':
session = Prompt()

answer = session.prompt(">> ", rprompt="<brown><i>Quo</i></brown>")
echo("You said: %s" % answer)

# Option 2 pass a string with red background color
session = Prompt()

answer = session.prompt(">> ", rprompt="<style bg='red' fg='green'>Quo</style>")
echo("You said: %s" % answer)

# Option 3 pass a bold string with blue background color
session = Prompt()
answer = session.prompt(">> ", rprompt="<style bg='blue'><b>Quo</b></style>")
echo(f"You said: {answer}")
