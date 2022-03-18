from quo.console import console
from quo.keys import bind
from quo.shortcuts import container
from quo.style import Style

from quo.widget import Box, Label, Frame, Shadow
from quo.layout import HSplit, VSplit, Window, FormattedTextControl
from quo.text import Text


def get_time():
    "Tokens to be shown before the prompt."
    import datetime

    now = datetime.datetime.now()
    return [
            ("reverse", "FEATURES | press `q` or `ctrl-c` to quit "),
            ("fg:green", "%s:%s:%s"  % (now.hour, now.minute, now.second))
            ]



content = HSplit([
    Window(
        FormattedTextControl(get_time), style="reverse", height=1, align="centre"), #"FEATURES | press `q` or `ctrl-c` to quit" + get_time), style="reverse", height=1, align="center"),
    Label(
            Text('<red>*</red><b> Support for ANSI, RGB and Hex color models.</b>\n<blue>*</blue><b> Support for tabular presentation of data.</b>\n<green>*</green><b> Intuitive progressbars.</b>\n<magenta>*</magenta><b> Syntax <style fg="yellow" bg="red">Highlighting</style></b>\n<yellow>*</yellow><b> Nesting of Commands.</b>\n<teal>*</teal><b> Automatic help page generation.</b>\n<khaki>*</khaki><b> Key bindings.</b>\n<aquamarine>*</aquamarine><b> Auto suggestions.</b>\n<brown>*</brown><b> Customizable Text User Interface<i>(TUI)</i> dialogs</b>'
                        ),
                    ),
        Window(height=1, char='\u2501'),
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
        Window(height=1, char="\u2501"),
        Window(FormattedTextControl("Press Ctrl-D to donate 🎁", style="fg:yellow bg:purple"))
])

@bind.add("ctrl-d")
def _(event):
    console.launch("https://ko-fi.com/scalabli")
@bind.add("q")
def _(event):
    event.app.exit()
@bind.add("ctrl-c")
def _(event):
    event.app.exit()

container(content, bind=True, full_screen=True, refresh=0.5)
