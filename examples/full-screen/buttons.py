#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
import quo

from quo.suite.current import get_app

from quo.keys.key_binding.bindings.focus import focus_next, focus_previous
from quo.styles import Style



# Event handlers for all the buttons.
def button1_clicked():
    text_area.text = "Button 1 clicked"


def button2_clicked():
    text_area.text = "Button 2 clicked"


def button3_clicked():
    text_area.text = "Button 3 clicked"


def exit_clicked():
    get_app().exit()


# All the widgets for the UI.


button1 = quo.widgets.Button("Button 1", handler=button1_clicked)
button2 = quo.widgets.Button("Button 2", handler=button2_clicked)
button3 = quo.widgets.Button("Button 3", handler=button3_clicked)
button4 = quo.widgets.Button("Exit", handler=exit_clicked)
text_area = quo.widgets.TextArea(focusable=True)


# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
root_container = quo.widgets.Box(
    quo.layout.HSplit(
        [
            quo.widgets.Label(text="Press `Tab` to move the focus."),
            quo.layout.VSplit(
                [
                    quo.widgets.Box(
                        body=quo.layout.HSplit([button1, button2, button3, button4], padding=1),
                        padding=1,
                        style="class:left-pane",
                    ),
                    quo.widgets.Box(body=quo.widgets.Frame(text_area), padding=1, style="class:right-pane"),
                ]
            ),
        ]
    ),
)

layout = quo.layout.Layout(container=root_container, focused_element=button1)


# Key bindings.
kb = quo.keys.KeyBinder()
kb.add("tab")(focus_next)
kb.add("s-tab")(focus_previous)


# Styling.
style = Style(
    [
        ("left-pane", "bg:#888800 #000000"),
        ("right-pane", "bg:#00aa00 #000000"),
        ("button", "#000000"),
        ("button-arrow", "#000000"),
        ("button focused", "bg:#ff0000"),
        ("text-area focused", "bg:#ff0000"),
    ]
)


# Build a main application object.
application = quo.Suite(layout=layout, key_bindings=kb, style=style, full_screen=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
