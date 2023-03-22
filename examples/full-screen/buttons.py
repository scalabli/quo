#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from quo import container
from quo.console import get_app
from quo.keys import bind, focus
from quo.layout import HSplit, VSplit
from quo.widget import Box, Button, Frame, Label, TextField
# Event handlers for all the buttons.
def button1():
    text_area.text = "Button 1 clicked"

def button2():
    text_area.text = "Button 2 clicked"


def button3():
    text_area.text = "Button 3 clicked"

def button4():    
    text_area.text = "Button 4 clicked"


def exit():
    get_app().exit()
def dd():
    content = Label("hello, world", style="fg:red bg:blue")
    container(content, bind=True, full_screen=True)

# All the widgets for the UI.


b1 = Button("Button 1", handler=button1)
b2 = Button("Button 2", handler=button2)
b3 = Button("Button 3", handler=button3)
b4 = Button("kenya", handler=button4)
b5 = Button("Exit", handler=exit)

text_area = TextField(scrollbar=True, focusable=True, style="fg:brown")

# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
content =  Box(
        HSplit(
            [
            Label("Press `Tab` to move the focus."),
            VSplit([
                Box(
                    HSplit([b1, b2, b3, b4, b5], 
                        padding=1),
                    padding=1,
                    style="bg:magenta"
                    ),
                Box(
                    Frame(
                        text_area,
                        title="Quo"
                        ),
                    padding=1, 
                    style="bg:blue fg:green"
                    )
                ]
            )
        ]
    )
)



# Key bindings.
bind.add("tab")(focus.next)
bind.add("s-tab")(focus.previous)

container(content, bind=True, focused_element=b3, full_screen=True)
