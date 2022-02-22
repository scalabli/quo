from quo import Console
from quo.widget import Box, Label
from quo.keys import KeyBinder
from quo.layout import Layout
from quo.style import Style

# Styling for the label
example_style = Style(
        [
            ("hello-world", "bg:red fg:black")
            ]
        )

root = Box(
        Label("Hello, World", style="class:hello-world"), padding=2)

layout = Layout(container=root)

kb = KeyBinder()

@kb.add("ctrl-c")
def _(event):
    event.app.exit()

Console(layout=layout, bind=kb, style=example_style, full_screen=True).run()

