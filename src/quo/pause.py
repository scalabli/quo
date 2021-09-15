import sys
from .interpose import interpose
from .accordance import isatty
from quo.expediency import inscribe
from quo.i_o.termui import echo



def pause(
        info="Press any key to proceed >> ...", 
        err=False
        ):
    """This command stops execution and waits for the user to press any key to continue.  This is similar to the Windows batch "pause"
    command.  If the program is not run through a terminal, this command
    will instead do nothing.

    :param info: the info string to print before pausing.
    :param err: if set to message goes to ``stderr`` instead of
                ``stdout``, the same as with echo.
    """
    if not isatty(sys.stdin) or not isatty(sys.stdout):
        return
    try:
        if info:
            echo(info, nl=False, err=err)
        try:
            interpose()
        except (KeyboardInterrupt, EOFError):
            pass
    finally:
        if info:
            inscribe(err=err)
