#!/usr/bin/env python
"""
Demonstration of a custom clipboard class.
This requires the 'pyperclip' library to be installed.
"""
import quo

session = quo.Prompt()

if __name__ == "__main__":
    print("Emacs shortcuts:")
    print("    Press Control-Y to paste from the system clipboard.")
    print("    Press Control-Space or Control-@ to enter selection mode.")
    print("    Press Control-W to cut to clipboard.")
    print("")

    answer = session.prompt("Give me some input: ", clipboard=quo.clipboard.PyperClipboard())
    quo.echo(f"You said: {answer}")
