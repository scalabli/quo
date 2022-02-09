#!/usr/bin/env python
"""
An example of a BufferControl in a full screen layout that offers auto
completion.

Important is to make sure that there is a `CompletionsMenu` in the layout,
otherwise the completions won't be visible.
"""
import quo

from quo.layout.controls import BufferControl, FormattedTextControl


# The completer.
animal_completer = quo.completion.WordCompleter(
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
    ],
    ignore_case=True,
)


# The layout
buff = quo.buffer.Buffer(completer=animal_completer, complete_while_typing=True)

body = quo.layout.FloatContainer(
    content=quo.layout.HSplit(
        [
            quo.layout.Window(
                FormattedTextControl('Press "q" to quit.'), height=1, style="reverse"
            ),
            quo.layout.Window(BufferControl(buffer=buff)),
        ]
    ),
    floats=[
        quo.layout.Float(
            xcursor=True,
            ycursor=True,
            content=quo.layout.CompletionsMenu(max_height=16, scroll_offset=1),
        )
    ],
)


# Key bindings
kb = quo.keys.KeyBinder()


@kb.add("q")
@kb.add("ctrl-c")
def _(event):
    "Quit application."
    event.app.exit()


# The `Application`
application = quo.Suite(layout=quo.layout.Layout(body), bind=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
