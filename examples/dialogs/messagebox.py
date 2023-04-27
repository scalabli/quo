#!/usr/bin/env python
"""
Example of a message box window.
"""
from quo.dialog import MessageBox

MessageBox(
        title="Message window",
        text="<red>Do you want to continue?\nPress ENTER to quit.</red>",
        bg=True
        )

