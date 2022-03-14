#!/usr/bin/env python
"""
Example of an input box dialog.
"""
from quo import echo
from quo.dialog import InputBox
from quo.completion import WordCompleter

result = InputBox(
        title="PromptBox shenanigans", 
        text="What Country are you from?:")

echo(f"Result = {result}")

