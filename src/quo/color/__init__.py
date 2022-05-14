from .ansi import ansi_color_codes, _ansi_reset_all, ANSI_COLOR_NAMES
from quo.output.color import ColorDepth
from quo.style.webcolors import NAMED_COLORS
from .rgb import *

def Color(color:str = None):
    #User input (default text color)
    from quo.style.style import Style

    return Style.add({' ':color})

