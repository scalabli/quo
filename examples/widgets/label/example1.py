from quo import Console
from quo.widget import Label
from quo.keys import KeyBinder
from quo.layout import Layout
from quo.style import Style

# Styling for the label
example = Style(
        [
            ("hello-world", "bg:red fg:black")
            ]
        )

root = Label("Hello, World", style="class:hello-world")

layout = Layout(container=root)

kb = KeyBinder()

@kb.add("ctrl-c")
def _(event):
    event.app.exit()

Console(layout=layout, bind=kb, style=example, full_screen=True).run()

