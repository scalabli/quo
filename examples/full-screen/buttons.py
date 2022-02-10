#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
import quo


# Event handlers for all the buttons.
def button1():
    get_app()
    text_area.text = "Button 1 clicked"


def button2():
    text_area.text = "Button 2 clicked"

import os 
def button3():
    text_area.text = os.system("ls") # "Button 3 clicked"


def exit():
    get_app().exit()


# All the widgets for the UI.


b1 = quo.widgets.Button("Button 1", handler=button1)
b2 = quo.widgets.Button("Button 2", handler=button2)
b3 = quo.widgets.Button("Button 3", handler=button3)
b4 = quo.widgets.Button("Exit", handler=exit)
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
                        body=quo.layout.HSplit([b1, b2, b3, b4], padding=1),
                        padding=1,
                        style="class:left-pane",
                    ),
                    quo.widgets.Box(body=quo.widgets.Frame(text_area), padding=1, style="class:right-pane"),
                ]
            ),
        ]
    ),
)

layout = quo.layout.Layout(container=root_container, focused_element=b1)


# Key bindings.
kb = quo.keys.KeyBinder()

kb.add("tab")(quo.keys.focus.next)
kb.add("s-tab")(quo.keys.focus.previous)


# Styling.

styling = quo.styles.Style

style = styling(
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
application = quo.console.Console(layout=layout, bind=kb, style=style, full_screen=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
