#!/usr/bin/env python
"""
Example of an input box dialog.
"""
from quo import echo
from quo.dialog import PromptBox

result = PromptBox(
        title="PromptBox shenanigans", text="What Country are you from?:").run()

echo(f"Result = {result}")

