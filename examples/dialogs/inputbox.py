#!/usr/bin/env python
"""
Example of an input box dialog.
"""
from quo import print
from quo.dialog import InputBox

result = InputBox(
        title="PromptBox shenanigans", 
        text="What Country are you from?:",)

print(f"Result = {result}")

