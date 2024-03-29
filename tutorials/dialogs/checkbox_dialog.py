#!/usr/bin/env python
"""
Example of a checkbox-list-based dialog.
"""
from quo import HTML
from quo.shortcuts import checkboxlist_dialog, message_dialog
from quo.styles import Style

results = checkboxlist_dialog(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", HTML("<blue>Bacon</blue>")),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
    style=Style.from_dict(
        {
            "dialog": "bg:#cdbbb3",
            "button": "bg:#bf99a4",
            "checkbox": "#e8612c",
            "dialog.body": "bg:#a9cfd0",
            "dialog shadow": "bg:#c98982",
            "frame.label": "#fcaca3",
            "dialog.body label": "#fd8bb6",
        }
    ),
).run()
if results:
    message_dialog(
        title="Room service",
        text="You selected: %s\nGreat choice sir !" % ",".join(results),
    ).run()
else:
    message_dialog("*starves*").run()
