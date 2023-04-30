"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""

import os
import sys

#from .pause import pause as pause
from .prompt import (
    prompt as prompt,
)  # dont confuse this with :class: quo.prompt.Prompt()



def clear() -> None:

    """Clears the terminal screen and moves the cursor to the top left.
       :return: None
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    

def exit(code: int):

    """
    Exit the interpreter immediately using os._exit()

    This function provides a low-level exit that bypasses the normal Python
    shutdown process and immediately terminates the interpreter. This can
    be useful in situations where a faster exit is needed, such as shell
    completion or other interactive applications.

    Args:
        code (int, optional): The exit status code. Defaults to 0.

    Returns:
        None
    """
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)


def getchar():
    """
    Get a single character from standard input.

    This function reads a single character from standard input (stdin)
    and returns it as a string. If an end-of-file (EOF) character is
    encountered, this function returns an empty string.

    Note that this function may behave differently depending on the
    operating system and the terminal emulator being used. In some cases,
    certain special characters (such as arrow keys or function keys) may
    not be interpreted correctly.

    Returns:
          str: A single character read from standard input, or an empty
             string if an end-of-file character is encountered.
    """
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char


def print(
        *values, #: Any,
        end="\n ",
        include_default_pygments_style=None,
        sep=" ",
        style=None,
        output=None,
        colorDepth=None,
        style_transformation=None
        ) ->None:

    from quo.shortcuts.utils import _print
    from quo.text.html import Text
    _print(Text(*values), end=end, include_default_pygments_style=include_default_pygments_style, color_depth=colorDepth, style=style, output=output, sep=sep, style_transformation=style_transformation)
        
    
def pause(message: str ='Press any key to continue »...'):
    """
    Pause execution and wait for the user to press any key.

    This function displays a message (default 'Press any key to continue...')
    and waits for the user to press any key before continuing execution.
    The message is displayed on standard output (stdout), and user input is
    read from standard input (stdin).

    Note that this function may behave differently depending on the
    operating system and the terminal emulator being used. In some cases,
    certain special characters (such as arrow keys or function keys) may
    not be interpreted correctly.

    Args:
        message (str, optional): The message to display before waiting for
                                 user input. Defaults to 'Press any key to continue...'.

    Returns:
        None
    """

    print(message)
    if sys.platform.startswith('win'):
        import msvcrt
        msvcrt.getch()
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
#from quo.shortcuts.utils import print
from quo.i_o.termui import confirm, echo
from quo.shortcuts.utils import container

__version__ = "2023.5.1"
