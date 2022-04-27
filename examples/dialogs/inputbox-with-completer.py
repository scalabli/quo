#!/usr/bin/env python
"""
Example of an input box dialog.
"""
from quo import print
from quo.completion import WordCompleter
from quo.dialog import InputBox

words = WordCompleter(["USA", "UK", "GERMANY", "KENYA"])
result = InputBox(
        title="PromptBox shenanigans", 
        text="What Country are you from?:",
        completer=words,
        multiline=True,
        bg=False)

print(f"Result = {result}")

