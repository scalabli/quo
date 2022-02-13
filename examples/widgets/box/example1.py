from quo import Console
from quo.widgets import Box, Label
from quo.keys import KeyBinder
from quo.layout import Layout, HSplit
from quo.style import Style

# Styling for the label
example_style = Style(
        [
            ("hello-world", "bg:red fg:black")
            ]
        )

root = Box(
        HSplit(
            [                                                     Label("Hello, World", style="class:hello-world")
                ]
            ), padding=2, char="|")

layout = Layout(container=root)

kb = KeyBinder()

@kb.add("ctrl-c")
def _():
    app.exit()

Console(layout=layout, bind=kb, style=example_style, full_screen=True).run()

