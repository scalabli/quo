from quo.shortcuts import container
from quo.style import Style

from quo.console import Console

from quo.widget import Box, Label, Frame
from quo.layout import Layout, HSplit, Window, WindowAlign as WA, FormattedTextControl
from quo.keys import KeyBinder
from quo.text import Text

console = Console()


container(
        Frame(
            Label(Text('      <reverse>QUO FEATURES»»»</reverse>')),
                title=Text('<u><b><reverse>Quo</reverse></b></u>')
        
        
            ))

root =  Box(
        Label(
            Text('<red>*</red><b> Support for ANSI, RGB and Hex color models.</b>\n<blue>*</blue><b> Support for tabular presentation of data.</b>\n<green>*</green><b> Intuitive progressbars.</b>\n<magenta>*</magenta><b> Syntax <style fg="yellow" bg="red">Highlighting</style></b>\n<yellow>*</yellow><b> Nesting of Commands.</b>\n<teal>*</teal><b> Automatic help page generation.</b>\n<khaki>*</khaki><b> Key bindings.</b>\n<aquamarine>*</aquamarine><b> Auto suggestions.</b>\n<brown>*</brown><b> Customizable Text User Interface<i>(TUI)</i> dialogs</b>'
                        )
                    )
        )
root1 = Label(
        Text('<style fg="aquamarine" bg="purple"> Press Ctrl-L to launch the documentation</style>'))

layout = Layout(root)
layout1 = Layout(root1)
kb = KeyBinder()
@kb.add("ctrl-l")
def _(event):
    console.launch("https://quo.rtfd.io")
@kb.add("<any>")
def _(event):
    event.app.exit()

Console(layout=layout, full_screen=True, bind=kb).run()
Console(layout=layout1, full_screen=True, bind=kb).run()
