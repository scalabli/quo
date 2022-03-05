#!/usr/bin/env python
"""
get_password function that displays asterisks instead of the actual characters.
With the addition of a ControlT shortcut to hide/show the input.
"""
#from quo import Condition
from quo.prompt import Prompt, Toggle
from quo.keys import KeyBinder

#kb = KeyBinder()

#hidden = [True]  # Nonlocal

#@kb.add("ctrl-t")
#def _(event):
#    "When ControlT has been pressed, toggle visibility."
#    hidden[0] = not hidden[0]
#    print("\nType Control-T to toggle password visible.")

session = Prompt(hide=Toggle)# bind=kb)
#Condition(lambda: hidden[0]), bind=kb)

password = session.prompt( "Password: ")
print("You said: %s" % password)

