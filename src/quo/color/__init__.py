from .ansi import ansi_color_codes, _ansi_reset_all, ANSI_COLOR_NAMES
from quo.output.color import ColorDepth
from quo.style.webcolors import NAMED_COLORS
from .rgb import *


def Color(style:str="", fg:str="", bg:str=""):
    from quo.style.style import Style
    if fg or bg != "":
        return Style.add({' ':"fg:"+str(fg) + " bg:"+str(bg)})
    if style != "":
        return Style.add({' ':style})


