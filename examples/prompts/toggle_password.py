#!/usr/bin/env python
"""
get_password function that displays asterisks instead of the actual characters.
With the addition of a ControlT shortcut to hide/show the input.
"""
import quo

session = quo.Prompt()

def main():
    hidden = [True]  # Nonlocal
    bindings = quo.keys.KeyBinder()

    @bindings.add("ctrl-t")
    def _(event):
        "When ControlT has been pressed, toggle visibility."
        hidden[0] = not hidden[0]

    print("Type Control-T to toggle password visible.")
    password = session.prompt(
        "Password: ", is_password=quo.filters.Condition(lambda: hidden[0]), key_bindings=bindings
    )
    print("You said: %s" % password)


if __name__ == "__main__":
    main()
