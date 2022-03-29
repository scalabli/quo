#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from quo import container
from quo.console import get_app
from quo.keys import bind, focus
from quo.layout import HSplit, VSplit
from quo.widget import Box, Button, Frame, Label, TextArea


# Event handlers for all the buttons.
def button1():
    get_app()
    text_area.text = "Button 1 clicked"


def button2():
    text_area.text = "Button 2 clicked"


def button3():
    text_area.text = "Button 3 clicked"

def button4():
    get_app()
    lbl.style = "fg:red"

def exit():
    get_app().exit()


# All the widgets for the UI.


b1 = Button("Button 1", handler=button1)
b2 = Button("Button 2", handler=button2)
b3 = Button("Button 3", handler=button3)
b4 = Button("Exit", handler=exit)
b5 = Button("kenya", handler=button4)
text_area = TextArea(scrollbar=True, focusable=True, style="brown")
lbl = Label("dkekkrkr")


# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
content =  Box(
        HSplit(
            [
            Label(text="Press `Tab` to move the focus."),
            VSplit([
                Box(body=HSplit([b1, b2, b3, b4, b5], padding=1),
                        padding=1,
                        style="bg:magenta"),
                Box(body=Frame(text_area, title="eee"), padding=1, style="bg:blue fg:green")
                ]
            ),
        ]
    )
)



# Key bindings.
bind.add("l")(focus.last)
bind.add("tab")(focus.next)
bind.add("s-tab")(focus.previous)

container(content, bind=True, focused_element=b1, full_screen=True)
