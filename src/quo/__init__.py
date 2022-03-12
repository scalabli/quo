"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib

from quo.exit import quick_exit as exit
from quo.console.console import Console as Console
from .core import Context as Clime
from .core import Parameter as Parameter
from .core import App as App 
from .core import Tether as Tether
from .getchar import getchar as getchar
from .pause import pause as pause
from .prompt import prompt as prompt  # dont confuse this with :class: quo.prompt.Prompt()
from quo.filters.core import Condition as Condition
from quo.shortcuts import print as print




#             Arg,
#             BaseCommand,
#             Command,
#             CommandCollection,
#             MultiCommand,



#from quo.accordance import (
#        DEFAULT_COLUMNS,
#        get_winterm_size,
#        strip_ansi_colors
#        )

#from quo.context.current import resolve_color_default
#from quo.expediency import inscribe # LazyFile



#from quo.decorators import (
                #       app,
 #                      arg,
            #           command,
                   #    tether
       #               )

from quo.decorators import (
             contextualize,
#             objectualize,
             make_pass_decorator
#             autoversion,
#             autopasswd,
#             autohelp,
#             autoconfirm
)

#from .setout import HelpFormatter, wraptext
from quo.context.current import currentcontext as pass_clime
#from .parser import AppParser

from quo.expediency import (
    appdir,
    formatfilename,
    os_args,
    textstream,
    binarystream,
    )
        

def clear():
    import sys
    import os
    from .accordance import isatty, WIN
    """Clears the terminal screen and moves the cursor to the top left.
    """
    if not isatty(sys.stdout):
        return

    if WIN:
        os.system("class")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


from quo.i_o import (
              confirm,
              echo
              )

from quo.shortcuts import container

__version__ = "2022.3.1"
