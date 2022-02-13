#!/usr/bin/env python
"""
Demonstration of a custom clipboard class.
This requires the 'pyperclip' library to be installed.
"""
from quo import echo
from quo.clipboard import PyperClipboard
from quo.prompt import Prompt

session = Prompt()

if __name__ == "__main__":
    print("Emacs shortcuts:")
    print("    Press Control-Y to paste from the system clipboard.")
    print("    Press Control-Space or Control-@ to enter selection mode.")
    print("    Press Control-W to cut to clipboard.")
    print("")

    answer = session.prompt("Give me some input: ", clipboard=PyperClipboard())
    echo(f"You said: {answer}")
