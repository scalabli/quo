#!/usr/bin/env python
"""
Example of a checkbox-list-based dialog.
"""
import quo

styling = quo.styles.Style

results = quo.CheckBox(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", quo.text.HTML("<blue>Bacon</blue>")),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
    style=styling.add(
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
    quo.MessageBox(
        title="Room service",
        text="You selected: %s\nGreat choice sir !" % ",".join(results),
    ).run()
else:
    quo.MessageBox("*starves*").run()
