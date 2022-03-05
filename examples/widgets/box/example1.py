from quo.console import Console
from quo.widget import Box, Label
from quo.keys import Bind
from quo.layout import Layout


root = Box(
        Label("Hello, World", style="bg:red fg:black"), padding=2)

layout = Layout(root)

bind = Bind()

@bind.add("ctrl-c")
def _(event):
    event.app.exit()

Console(layout=layout, bind=bind, full_screen=True).run()

