#!/usr/bin/env python
"""
A simple example of a calculator program.
This could be used as inspiration for a REPL.
"""

from quo import container
from quo.document import Document
from quo.keys import bind
from quo.layout import HSplit
from quo.textfield import TextField
from quo.toolbar import SearchToolbar
from quo.window import Window

help_text = """
            Type any expression (e.g. "4 + 4") followed by enter to execute.
            Press Control-C to exit.
            """


# The layout.
searchField = SearchToolbar()  # For reverse search.

outputField = TextField(text=help_text, style="bg:blue fg:yellow bold", multiline=True)

inputField = TextField(
                height=5, 
                prompt=">>", 
                style="bg:gray fg:green", 
                wrap_lines=True,
                search_field=searchField,
                )

content = HSplit([
            outputField,
            Window(height=1, char="-", style="fg:magenta"),
            inputField,
           # searchField,
        ])

# Attach accept handler to the input field. We do this by assigning the
# handler to the `TextArea` that we created earlier. it is also possible to
# pass it to the constructor of `TextArea`.
# NOTE: It's better to assign an `accept_handler`, rather then adding a
#       custom ENTER key binding. This will automatically reset the input
#       field and add the strings to the history.
def accept(buff):
     # Evaluate "calculator" expression.
    try:
        output = "\n\nIn:  {}\nOut: {}".format(
            inputField.text, eval(inputField.text)
            )  # Don't do 'eval' in real code!

    except BaseException as e:
        output = "\n\n{}".format(e)
        newText = outputField.text + output
        # Add text to output buffer.
        outputField.buffer.document = Document(
            text=newText, cursor_position=len(newText)
            )
inputField.accept_handler = accept

print(inputField.text)

# The key bindings.
# "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
container(
    content,
    bind=True,
    focused_element=inputField,
    full_screen=True,
    mouse_support=True,
    )
