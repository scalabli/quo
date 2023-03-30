#!/usr/bin/env python
"""
An example of a BufferControl in a full screen layout that offers auto
completion.

Important is to make sure that there is a `CompletionsMenu` in the layout,
otherwise the completions won't be visible.
"""
from quo import container
from quo.buffer import Buffer
from quo.completion import WordCompleter
from quo.layout import BufferControl, FormattedTextControl, FloatContainer, Float, CompletionsMenu, HSplit, Window
# The completer.
animal_completer = WordCompleter(
    [
        "alligator",
        "ant",
        "ape",
        "bat",
        "bear",
        "beaver",
        "bee",
        "bison",
        "butterfly",
        "cat",
        "chicken",
        "crocodile",
        "dinosaur",
        "dog",
        "dolphin",
        "dove",
        "duck",
        "eagle",
        "elephant",
        "fish",
        "goat",
        "gorilla",
        "kangaroo",
        "leopard",
        "lion",
        "mouse",
        "rabbit",
        "rat",
        "snake",
        "spider",
        "turkey",
        "turtle",
    ]
    )


# The layout
buff = Buffer(completer=animal_completer, complete_while_typing=True)

content = FloatContainer(
        HSplit([
            Window(
                FormattedTextControl('Press "ctrl-c" to quit.'), height=1, style="reverse"),
            Window(BufferControl(buff))
            ]),
        floats=[
            Float(
                xcursor=True,
                ycursor=True,
                content = CompletionsMenu(max_height=16, scroll_offset=1),
        )
    ]
        )



# The `Application`

container(content, bind=True, full_screen=True)
