#!/usr/bin/env python
"""
Simple example of a full screen application with a vertical split.

This will show a window on the left for user input. When the user types, the
reversed input is shown on the right. Pressing Ctrl-Q will quit the application.
"""
from quo import container
from quo.buffer import Buffer
from quo.keys import bind
from quo.layout.controls import BufferControl, FormattedTextControl
from quo.layout import VSplit, HSplit
from quo.window import Window

# 3. Create the buffers
#    ------------------

leftBuffer = Buffer()
rightBuffer =Buffer()

# 1. First we create the layout
#    --------------------------

leftWindow = Window(BufferControl(leftBuffer))
rightWindow = Window(BufferControl(rightBuffer))



# A vertical line in the middle. We explicitly specify the width, to make
# sure that the layout engine will not try to divide the whole width by
# # three for all these windows.

verticalLine = Window(width=1, char="|", style="class:line")


body = VSplit([

        leftWindow,
        verticalLine,
        # Display the Result buffer on the right.
        rightWindow
    ])

# As a demonstration. Let's add a title bar to the top, displaying "Hello world".

# somewhere, because usually the default key bindings include searching. (Press
# Ctrl-R.) It would be really annoying if the search key bindings are handled,
# but the user doesn't see any feedback. We will add the search toolbar to the
# bottom by using an HSplit.


def get_titlebar_text():
    return [
        ("class:title", " Hello world "),
        ("class:title", " (Press [Ctrl-Q] to quit.)"),
    ]


rootContainer = HSplit(
    [
        # The titlebar.
        Window(
            height=1,
            content=FormattedTextControl(get_titlebar_text),
            align="center"
        ),
        # Horizontal separator.
        Window(height=1, char="-", style="class:line"),
        # The 'body', like defined above.
        body,
    ]
)


# 2. Adding key bindings
#   --------------------

# As a demonstration, we will add just a ControlQ key binding to exit the
# application.

# Now add the Ctrl-Q binding. We have to pass `eager=True` here. The reason is
# that there is another key *sequence* that starts with Ctrl-Q as well. Yes, a
# key binding is linked to a sequence of keys, not necessarily one key. So,
# what happens if there is a key binding for the letter 'a' and a key binding
# for 'ab'. When 'a' has been pressed, nothing will happen yet. Because the
# next key could be a 'b', but it could as well be anything else. If it's a 'c'
# for instance, we'll handle the key binding for 'a' and then look for a key
# binding for 'c'. So, when there's a common prefix in a key binding sequence,
# prompt-toolkit will wait calling a handler, until we have enough information.

# Now, There is an Emacs key binding for the [Ctrl-Q Any] sequence by default.
# Pressing Ctrl-Q followed by any other key will do a quoted insert. So to be
# sure that we won't wait for that key binding to match, but instead execute
# Ctrl-Q immediately, we can pass eager=True. (Don't make a habit of adding
# `eager=True` to all key bindings, but do it when it conflicts with another
# existing key binding, and you definitely want to override that behaviour.


@bind.add("ctrl-c", eager=True)
@bind.add("ctrl-q", eager=True)
def _(event):
    """
    Pressing Ctrl-Q or Ctrl-C will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.

    Note that Ctrl-Q does not work on all terminals. Sometimes it requires
    executing `stty -ixon`.
    """
    event.app.exit()


# Now we add an event handler that captures change events to the buffer on the
# left. If the text changes over there, we'll update the buffer on the right.


def default_buffer_changed(_):
    """
    When the buffer on the left changes, update the buffer on
    the right. We just reverse the text.
    """
    rightBuffer.text = leftBuffer.text[::-1]


leftBuffer.on_text_changed += default_buffer_changed


# This glues everything together.
container(rootContainer, focused_element=leftWindow, bind=True,  mouse_support=True,full_screen=True)

#application = Console(
 #       layout=layout,
  #      bind=kb,
    # Let's add mouse support!
    # Using an alternate screen buffer means as much as: "run full screen".
    # It switches the terminal to an alternate screen.
    #    full_screen=True,
        