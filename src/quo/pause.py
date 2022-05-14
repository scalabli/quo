def pause(info: str = "Press any key to proceed »...", err: bool = False):
    """This command stops execution and waits for the user to press any key to continue.  This is similar to the Windows batch "pause"
    command.  If the program is not run through a terminal, this command
    will instead do nothing.

    :param info: the info string to print before pausing.
    :param err: if set to message goes to ``stderr`` instead of
                ``stdout``, the same as with echo.
    """
    import sys

    from .accordance import isatty

    if not isatty(sys.stdin) or not isatty(sys.stdout):
        return
    try:
        if info:
            from quo.i_o.termui import echo

            echo(info, nl=False, err=err)
        try:
            from quo import getchar

            getchar()
        except (KeyboardInterrupt, EOFError):
            pass
    finally:
        if info:
            from quo.expediency.vitals import inscribe

            inscribe(err=err)
