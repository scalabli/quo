#!/usr/bin/env python
"""
Example of button dialog window.
"""

from quo import echo
from quo.dialog import ChoiceBox

result = ChoiceBox(
        title="ChoiceBox example",
        text="Are you sure?",
        buttons= [("Yes", True), ("No", False), ("Maybe...", None)]).run()

if result == True:
    echo(f"Result = {result}")
