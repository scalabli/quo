#!/usr/bin/env python3
"""
Example of a right prompt. This is an additional prompt that is displayed on
the right side of the terminal. It will be hidden automatically when the input
is long enough to cover the right side of the terminal.

This is similar to RPROMPT is Zsh.
"""
from quo import echo
from quo.text import Text
from quo.prompt import Prompt

def main():
    # Option 1: pass a string to 'rprompt':
    rprompt = Text("<brown><i>Quo</i></brown>")
    session = Prompt(rprompt=rprompt)

    answer = session.prompt(">> ")
    echo("You said: %s" % answer)

    # Option 2

    rprompt = Text("<style bg='red' fg='green'>Quo</style>")
    session = Prompt(rprompt=rprompt)

    answer = session.prompt(">> ")
    echo("You said: %s" % answer)

    # Option 3

    rprompt = Text("<style bg='blue'>Quo</style>")
    session = Prompt(rprompt=rprompt)
    answer = session.prompt(">> ")
    echo(f"You said: {answer}")

if __name__ == "__main__":
    main()
