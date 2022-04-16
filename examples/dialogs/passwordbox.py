#!/usr/bin/env python
"""
Example of an password input dialog.
"""
from quo import print
from quo.dialog import InputBox

result = InputBox(
        title="Password dialog example",
        text="Please type your password:",
        hide=True)

print(f"{result}")

