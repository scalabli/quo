#!/usr/bin/env python
"""
A few examples of displaying a bottom toolbar.

The ``Prompt`` function takes a ``bottom_toolbar`` attribute.
This can be any kind of formatted text (plain text, or HTML), or
it can be a callable that takes an App and returns an of these.

The bottom toolbar will always receive the style 'bottom-toolbar', and the text
inside will get 'bottom-toolbar.text'. These can be used to change the default
style.
"""
import time
from quo import echo
from quo.prompt import Prompt


session = Prompt()

# Example 1: fixed text.
text = session.prompt("Say something: ", bottom_toolbar="This is quo toolbar")
echo(f"You said: {text}")

# Example 2: fixed text from a callable:

text = session.prompt("Say something: ", bottom_toolbar="Bottom toolbar: time=%r" % time.time(), refresh_interval=0.5)
echo(f"You said: {text}")

# Example 3: Using HTML:
text = session.prompt("Say something: ", bottom_toolbar='<b>This</b> <u>is</u> a <style bg="red">toolbar</style>')
echo(f"You said: {text}")

# Example 4: multiline fixed text.
text = session.prompt("Say something: ", bottom_toolbar="This is\na multiline toolbar")
print("You said: %s" % text)

