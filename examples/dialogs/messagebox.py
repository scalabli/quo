#!/usr/bin/env python
"""
Example of a message box window.
"""
from quo import echo, MessageBox

MessageBox(
        title="Message pop up window",
        text="Do you want to continue?\nPress ENTER to quit.").run()

