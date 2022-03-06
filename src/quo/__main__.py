from quo import print

from quo.shortcuts import container
from quo.style import Style
from quo.buffer import Buffer
from quo.console import Console
from quo.widget import Box, Label, Frame, Shadow
from quo.layout import Layout, HSplit, VSplit, Window, WindowAlign as WA, FormattedTextControl, BufferControl
from quo.layout.margin import NumberedMargin, ScrollbarMargin
from quo.keys import KeyBinder
from quo.text import Text, FormattedText

console = Console()

LIPSUM = ( """Quo is scallable\n"""* 3)
buff = Buffer()
buff.text = LIPSUM

root = HSplit([
    Window(
        FormattedTextControl("FEATURES | press `q` or `ctrl-c` to quit"), style="reverse", height=1, align=WA.CENTER),
    Label(
            Text('<red>*</red><b> Support for ANSI, RGB and Hex color models.</b>\n<blue>*</blue><b> Support for tabular presentation of data.</b>\n<green>*</green><b> Intuitive progressbars.</b>\n<magenta>*</magenta><b> Syntax <style fg="yellow" bg="red">Highlighting</style></b>\n<yellow>*</yellow><b> Nesting of Commands.</b>\n<teal>*</teal><b> Automatic help page generation.</b>\n<khaki>*</khaki><b> Key bindings.</b>\n<aquamarine>*</aquamarine><b> Auto suggestions.</b>\n<brown>*</brown><b> Customizable Text User Interface<i>(TUI)</i> dialogs</b>'
                        ),
                    ),
        Window(height=1, char='_'),
        VSplit([
                   Frame(
                       Label(
                           Text('<b> » Bold</b>    <b> »</b> <u>Underlined</u>\n<b> »</b> <i>Italic</i>  <b> »</b> <reverse>Reverse</reverse>\n<b> »</b> <s>Strike</s>  <b> »</b><hidden>Hidden</hidden> (Hidden)'),
                       ), title=Text('<u><orange>Formatted text</orange></u>'),
                   ),

                   Frame(
                       Label(
                           Text(" <red>Red</red> <yellow>Yellow</yellow> <green>Green</green> <gold>Gold</gold>\n <cyan>Cyan</cyan> <blue>Blue</blue> <gray>Gray</gray> <maroon>Maroon</maroon>\n <brown>Brown</brown> <aquamarine>Aquamarine</aquamarine> <teal>Teal</teal>")
                           ), title=Text('<u><dodgerblue>Colors</dodgerblue></u>'),
                       )
                ]),
        VSplit([
                Label(Text("<b> »</b> <gold>1 bit</gold>\n<b> »</b> <purple>4 bit</purple>\n<b> »</b> <red>8 bit</red>\n<b> »</b> <indigo>24 bit(True color)</indigo>")),
                Shadow(
                    Frame(
                    Label(
                        Text(' <b> <style fg="red" bg="gold">Red on gold  </style>  <gonp fg="green" bg="purple">Green on purple</gonp>\n  <style fg="cyan" bg="blue">Cyan on blue </style>  <style fg="white" bg="red">White on red   </style>\n  <style fg="teal" bg="white">Teal on white</style>  <style fg="black" bg="orange">Black on orange</style></b>')
                        ), title=Text('<u><red>Background colors</red></u>'),)
                    ),
                
            ]),
        Window(height=1, char="_"),
        HSplit([
            Window(FormattedTextControl('Margins.'), height=1, style="fg:red bg:yellow bold", align=WA.CENTER),
            Window(
        
                    BufferControl(buffer=buff),
                left_margins=[NumberedMargin(), ScrollbarMargin()],
                right_margins=[ScrollbarMargin(), ScrollbarMargin()],),


        ]),
        ])
root1 = Label(
        Text('<style fg="aquamarine" bg="purple"> Press Ctrl-L to launch the documentation</style>'))

layout = Layout(root)
layout1 = Layout(root1)
kb = KeyBinder()
@kb.add("ctrl-l")
def _(event):
    console.launch("https://quo.rtfd.io")
@kb.add("q")
def _(event):
    event.app.exit()
@kb.add("ctrl-c")
def _(event):
    event.app.exit()

Console(layout=layout, full_screen=True, bind=kb).run()
#Console(layout=layout1, full_screen=True, bind=kb).run()
