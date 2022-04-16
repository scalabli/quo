#!/usr/bin/env python
"""
Example of button dialog window.
"""

#from quo import echo
from quo.dialog import ChoiceBox

result = ChoiceBox(
        title="ChoiceBox example",
        text="Are you sure?",
        buttons= [
            ("Yes", True),
            ("No", False),
            ("Maybe...", None)]
        )
if result == True:
    print("dd")
  #  echo(f"Result = {result}")
