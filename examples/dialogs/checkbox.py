#!/usr/bin/env python
"""
Example of a checkbox-list-based dialog.
"""
#from quo import echo
from quo.dialog import CheckBox, MessageBox
from quo.text import Text
from quo.style import Style


style= Style.add({
    "dialog": "bg:#cdbbb3",
    "button": "bg:#bf99a4",
    "checkbox": "#e8612c",
    "dialog.body": "bg:#a9cfd0",
    "dialog shadow": "bg:#c98982",
    "frame.label": "#fcaca3",
    "dialog.body label": "#fd8bb6"})

results = CheckBox(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", Text("<blue>Bacon</blue>")),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
    bg=False
    )# style=style)

if results:
    MessageBox(
        title="Room service",
        text="You selected: %s\nGreat choice sir !" % ",".join(results))

else:
    MessageBox("*starves*", bg=False)
