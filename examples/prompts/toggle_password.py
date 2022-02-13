#!/usr/bin/env python
"""
get_password function that displays asterisks instead of the actual characters.
With the addition of a ControlT shortcut to hide/show the input.
"""
from quo import Condition
from quo.prompt import Prompt
from quo.keys import KeyBinder

session = Prompt()
kb = KeyBinder()
def main():
    hidden = [True]  # Nonlocal

    @kb.add("ctrl-t")
    def _(event):
        "When ControlT has been pressed, toggle visibility."
        hidden[0] = not hidden[0]

    print("Type Control-T to toggle password visible.")
    password = session.prompt( "Password: ", is_password=Condition(lambda: hidden[0]), bind=kb)
    print("You said: %s" % password)


if __name__ == "__main__":
    main()
