#!/usr/bin/env python
"""
Example of an password input dialog.
"""
from quo import echo, PromptBox

result = PromptBox(
        title="Password dialog example",
        text="Please type your password:",
        hide=True).run()

echo(f"{result}")

