import quo
from quo.i_o import echo
from quo.color.rgb import *
from quo.shortcuts import container
from quo.widget import Frame,Box, Label, TextArea
from quo.style import Style

style = Style(
        [
            ("lab", "reverse")
            ]
        )

root = Label("Quo",
        Box(
            Label("Features"), 
            padding=3
            ))
from quo.layout import Layout
from quo.keys import KeyBinder

kb = KeyBinder()
@kb.add("ctrl-c")
def _(event):
    event.app.exit()
layout = Layout(root)
from quo import Console
Console(
        layout=layout,
        bind=kb,
        style=style,
        full_screen=True).run()

    #(TextArea(text="         FEATURES"), title="Quo"))


echo(f"* ", fg="red", nl=False)
echo(f"Support for ANSI and RGB color models")
echo(f"* ", fg="blue", nl=False)
echo(f"Support for tabular presentation of data")
echo(f"* ", fg="green", nl=False)
echo(f"Interactive progressbars")
echo(f"* ", fg="magenta", nl=False)
echo(f"Code completions")
echo(f"* ", fg="yellow", nl=False)
echo(f"Nesting of commands")
echo(f"* ", fg=teal, nl=False)
echo(f"Automatic help page generation")
echo(f"* ", fg=aquamarine, nl=False)
echo(f"Highlighting")
echo(f"* ", fg=khaki, nl=False)
echo(f"Lightweight")

