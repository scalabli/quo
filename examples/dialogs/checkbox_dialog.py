#!/usr/bin/env python
"""
Example of a checkbox-list-based dialog.
"""
import quo

from quo.shortcuts import checkbox, message

results = checkbox(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", quo.text.HTML("<blue>Bacon</blue>")),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
    style=quo.styles.Style.add(
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
    message(
        title="Room service",
        text="You selected: %s\nGreat choice sir !" % ",".join(results),
    ).run()
else:
    message("*starves*").run()
