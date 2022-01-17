"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib

from quo.exit import quick_exit as exit
from quo.suite.suite import Suite
from .core import Context as Clime, Parameter
#             App,
#             Arg,
#             BaseCommand,
#             Command,
#             CommandCollection,
#             MultiCommand,
#             Parameter,
#             Tethe)



#from quo.accordance import (
#        DEFAULT_COLUMNS,
#        get_winterm_size,
#        strip_ansi_colors
#        )

#from quo.context.current import resolve_color_default
#from quo.expediency import inscribe # LazyFile
from quo.shortcuts.utils import inscribe
from quo.shortcuts import Prompt
from quo.pause import pause
from quo.shortcuts import message as MessageBox, evoke as PromptBox, progress as ProgressBox, radiolist as RadiolistBox, confirmation as ConfirmationBox, checkbox as CheckBox, choices as ChoiceBox
from quo.decorators import (
                       app,
                       arg,
                       command,
                       tether
                       )
from quo.progress import ProgressBar

#from quo.decorators import (
#             contextualize,
#             objectualize,
#             make_pass_decorator,
#             autoversion,
#             autopasswd,
#             autohelp,
#             autoconfirm
#             )

#from .setout import HelpFormatter, wraptext
#from quo.context.current import currentcontext
#from .parser import AppParser
from quo.expediency import (
                  appdir,
                  formatfilename,
                  os_args,
                  textstream,
                  binarystream,
                  openfile
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
              launch,
              echo,
              edit,
              terminalsize,
              unstyle,
              prompt,
              )

from quo.shortcuts import container

__version__ = "2022.1.6"
