#!/usr/bin/env python
"""
get_password function that displays asterisks instead of the actual characters.
With the addition of a ControlT shortcut to hide/show the input.
"""
from quo import Elicit, echo
from quo.filters import Condition
from quo.keys.key_binding import KeyBindings


def main():
    hidden = [True]  # Nonlocal
    kb = KeyBindings()

    @kb.add("c-t")
    def _(event):
        "When ControlT has been pressed, toggle visibility."
        hidden[0] = not hidden[0]

    echo("Type Control-T to toggle password visible.")

    s = Elicit()

    password = s.elicit(
        "Password: ", is_password=Condition(lambda: hidden[0]), key_bindings=kb
    )
    print("You said: %s" % password)


if __name__ == "__main__":
    main()
