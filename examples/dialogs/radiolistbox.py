#!/usr/bin/env python
"""
Example of a radio list box dialog.
"""
from quo.dialog import RadiolistBox
from quo.text import Text


result = RadiolistBox(
        values=[
            ("red", "Red"),
            ("green", "Green"),
            ("blue", "Blue"),
            ("orange", "Orange")
            ],
        title="Radiolist dialog example",
        text="Please select a color:")
print(f"Result = {result}")

# With Text
result = RadiolistBox(
            values=[
                ("red", '<style bg="red" fg="white">Red</style>'),
            ("green", Text('<style bg="green" fg="white">Green</style>')),
            ("blue", Text('<style bg="blue" fg="white">Blue</style>')),
            ("orange", Text('<style bg="orange" fg="white">Orange</style>')),
        ],
        title="RadiolistBox example <reverse>with colors</reverse>",
        text="<b><green>Please select a color:</green></b>")
print(f"Result = {result}")

