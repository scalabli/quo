#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from quo import container
from quo.box import Box
from quo.button import Button
from quo.console import application
from quo.keys import bind, focus
from quo.layout import HSplit, VSplit
from quo.label import Label
from quo.textfield import TextField


# Event handlers for all the buttons.
def button1():
    text_area.text = "You clicked button 1"

def button2():
    text_area.text = "You clicked button 2"

def button3():
    text_area.text = "You clicked button 3"

def button4():
    import datetime   
    text_area.text = f"You clicked button 4\nCurrent time is {datetime.datetime.now().strftime('%H:%M')}"
    
def exit():
    application().exit()


# All the widgets for the UI.

b1 = Button("Button 1", handler=button1)
b2 = Button("Button 2", handler=button2)
b3 = Button("Button 3", handler=button3)
b4 = Button("Button 4", handler=button4)
b5 = Button("Exit", handler=exit)

text_area = TextField(scrollbar=True, multiline=True, bg="black", fg="red")


label = Label("Press <maroon><b>`Tab`</b></maroon> or <gold><b>`Up and Down`</b></gold> keys to move focus")



mainBody = Box(text_area, bg="blue")

buttons = HSplit([b1, b2, b3, b4, b5], padding=1)
buttonsBody = Box(buttons, padding=1, bg="magenta")

# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
content =  Box(
        HSplit([
            label,
            VSplit([buttonsBody, mainBody])
        ]), 
        char="$"
        )

# Key bindings.
bind.add("tab")(focus.next)
bind.add("down")(focus.next)
bind.add("s-tab")(focus.previous)
bind.add("up")(focus.previous)


container(content, bind=True, full_screen=True)
