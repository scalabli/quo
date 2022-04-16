from typing import Optional

from quo.layout import Window, FormattedTextControl, WindowAlign as WA


def Bar(
    self, message: Optional[str] = None, align="center", style="fg:yellow bg:brown bold"
):
    from quo.shortcuts import container
    if align == "left":
        Window(FormattedTextControl(message), height=1, style=style, align=WA.LEFT)
    if align == "right":
        Window(FormattedTextControl(message), height=1, style=style, align=WA.RIGHT)
    if align == "center":
        content = Window(FormattedTextControl(message), height=1, style=style, align=WA.CENTER)
        container(content)


