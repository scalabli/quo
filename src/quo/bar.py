from typing import Optional
from quo.console import Console
from quo.shortcuts.utils import container
from quo.layout import Window, FormattedTextControl


def Bar(
        self, 
        text: Optional = None, 
        align="center", 
        style="fg:black bg:cyan"
        ) -> "Console":
    from quo.console.console import Console

    console = Console()

    return console.bar(message=text, align=align, style=style)

#(Window(FormattedTextControl(text), height=1, style=style, align=align))


