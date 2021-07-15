from quo.accordance import _default_text_stderr
from quo.accordance import _default_text_stdout
from quo.accordance import _find_binary_writer
from quo.accordance import auto_wrap_for_ansi
from quo.accordance import binary_streams
from quo.accordance import filename_to_ui
from quo.accordance import encoding_filesystem
from quo.accordance import get_strerror
from quo.accordance import is_bytes
from quo.accordance import openstream
from quo.accordance import should_strip_ansi_colors
from quo.accordance import strip_ansi_colors
from quo.accordance import text_streams
from quo.accordance import WIN
from quo.context.current import resolve_color_default


echo_functionality = (bytes, bytearray, str)



def echo(message=None, file=None, nl=True, err=False, color=None):
    """Prints a message plus a newline to the given file or stdout.  On
    first sight, this looks like the print function, but it has improved
    support for handling Unicode and binary data that does not fail no
    matter how badly configured the system is.

    Primarily it means that you can print binary data as well as Unicode
    data on both 2.x and 3.x to the given file in the most appropriate way
    possible.  This is a very carefree function in that it will try its
    best to not fail.  As of quo 6.0 this includes support for unicode
    output on the Windows console.

    In addition to that, if `colorama`_ is installed, the echo function will
    also support clever handling of ANSI codes.  Essentially it will then
    do the following:

    -   add transparent handling of ANSI color codes on Windows.
    -   hide ANSI codes automatically if the destination file is not a
        terminal.

    .. _colorama: https://pypi.org/project/colorama/


    :param message: the message to print
    :param file: the file to write to (defaults to ``stdout``)
    :param err: if set to true the file defaults to ``stderr`` instead of
                ``stdout``.  This is faster and easier than calling
                :func:`get_text_stderr` yourself.
    :param newline: if set to `True` (the default) a newline is printed afterwards.
    :param color: controls if the terminal supports ANSI colors or not.  The
                  default is autodetection.
    """
    if file is None:
        if err:
            file = _default_text_stderr()
        else:
            file = _default_text_stdout()

    """
    Convert non bytes/text into the native string type.
    """

    if message is not None and not isinstance(message, echo_functionality):
        message = str(message)

    if nl:
        message = message or ""
        if isinstance(message, str):
            message += "\n"
        else:
            message += b"\n"

    # If there is a message and the value looks like bytes, we manually
    # need to find the binary stream and write the message in there.
    # This is done separately so that most stream types will work as you
    # would expect. Eg: you can write to StringIO for other cases.
    if message and is_bytes(message):
        binary_file = _find_binary_writer(file)
        if binary_file is not None:
            file.flush()
            binary_file.write(message)
            binary_file.flush()
            return

    # ANSI-style support.  If there is no message or we are dealing with
    # bytes nothing is happening.  If we are connected to a file we want
    # to strip colors.  If we are on windows we either wrap the stream
    # to strip the color or we use the colorama support to translate the
    # ansi codes to API calls.
    if message and not is_bytes(message):
        color = resolve_color_default(color)
        if should_strip_ansi_colors(file, color):
            message = strip_ansi_colors(message)
        elif WIN:
            if auto_wrap_for_ansi is not None:
                file = auto_wrap_for_ansi(file)
            elif not color:
                message = strip_ansi_colors(message)

    if message:
        file.write(message)
    file.flush()

