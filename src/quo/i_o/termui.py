import inspect
import io
import itertools
import os
import struct
import sys
import math

from quo.accordance import (
        DEFAULT_COLUMNS,
        get_winterm_size,
        is_bytes,
        isatty,
        strip_ansi_colors,
        WIN
        )

from quo.outliers import Abort, UsageError
from quo.context.current import resolve_color_default
from quo.types import Choice, convert_type
from quo.expediency import inscribe, LazyFile
from quo.systematize.core import _isconvertible, _binary_type, _text_type, _bool_type

# The prompt functions to use.  The doc tools currently override these
# functions to customize how they work.
visible_prompt_func = input
#American National Standard Institute colors

ansi_color_codes = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "reset": 39,
    "vblack": 90,
    "vred": 91,
    "vgreen": 92,
    "vyellow": 93,
    "vblue": 94,
    "vmagenta": 95,
    "vcyan": 96,
    "vwhite": 97,
}
_ansi_reset_all = "\033[0m"


def hidden_prompt_func(prompt):
    import getpass

    return getpass.getpass(prompt)


def _build_prompt(
    text, suffix, show_default=False, default=None, show_choices=True, type=None
):
    prompt = text
    if type is not None and show_choices and isinstance(type, Choice):
        prompt += f" ({', '.join(map(str, type.choices))})"
    if default is not None and show_default:
        prompt = f"{prompt} [{_format_default(default)}]"
    return f"{prompt}{suffix}"


def _format_default(default):
    if isinstance(default, (io.IOBase, LazyFile)) and hasattr(default, "name"):
        return default.name

    return default

##################################################################
def prompt(
    text,
    default=None,
    hide=False,
    autoconfirm=False,
    type=None,
    value_proc=None,
    prompt_suffix=":> ",
    show_default=True,
    err=False,
    show_choices=True,
):

    """Prompts a user for input.  This is a convenience function that can be used to prompt a user for input later.

    If the user aborts the input by sending a interrupt signal, this  function will catch it and raise a :exc:`Abort` exception.

    :param text: the text to show for the prompt.
    :param default: the default value to use if no input happens.  If this  is not given it will prompt until it's aborted.
    :param hide_input: if this is set to true then the input value will  be hidden.
    :param autoconfirm: asks for confirmation for the value.
    :param type: the type to use to check the value against.
    :param value_proc: if this parameter is provided it's a function that is invoked instead of the type conversion to convert a value.
    :param prompt_suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of ``stdout``, the same as with echo.
    :param show_choices: Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is "Group by" then the  prompt will be "Group by (day, week): ".

    """
    result = None

    def prompt_func(text):
        f = hidden_prompt_func if hide else visible_prompt_func
        try:
            # Write the prompt separately so that we get nice
            # coloring through colorama on Windows
            inscribe(text, nl=False, err=err)
            return f("")
        except (KeyboardInterrupt, EOFError):
            # getpass doesn't print a newline if the user aborts input with ^C.
            # Allegedly this behavior is inherited from getpass(3).
            # A doc bug has been filed at https://bugs.python.org/issue24711
            if hide:
                inscribe(None, err=err)
            raise Abort()

    if value_proc is None:
        value_proc = convert_type(type, default)

    prompt = _build_prompt(
        text, prompt_suffix, show_default, default, show_choices, type
    )

    while 1:
        while 1:
            value = prompt_func(prompt)
            if value:
                break
            elif default is not None:
                value = default
                break
        try:
            result = value_proc(value)
        except UsageError as e:
            if hide:
                inscribe("Error: the value you entered was invalid", err=err)
            else:
                inscribe(f"Error: {e.message}", err=err)  # noqa: B306
            continue
        if not autoconfirm:
            return result
        while 1:
            value2 = prompt_func("Repeat for confirmation: ")
            if value2:
                break
        if value == value2:
            return result
        echo("Error: the two entered values do not match", err=err)
###########################################################################

def confirm(
        text, default=False, abort=False, prompt_suffix=":>", show_default=True, err=False
):
    """Prompts for confirmation (yes/no question).

    If the user aborts the input by sending a interrupt signal this
    function will catch it and raise a :exc:`Abort` exception.

    :param text: the question to ask.
    :param default: the default for the prompt.
    :param abort: if this is set to `True` a negative answer aborts the
                  exception by raising :exc:`Abort`.
    :param prompt_suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of
                ``stdout``, the same as with echo.
    """
    prompt = _build_prompt(
        text, prompt_suffix, show_default, "Yes/no" if default else "yes/No"
    )
    while 1:
        try:
            # Write the prompt separately so that we get nice
            # coloring through colorama on Windows
            echo(prompt, nl=False, err=err, fg="cyan")
            value = visible_prompt_func("").lower().strip()
        except (KeyboardInterrupt, EOFError):
            raise Abort()
        if value in ("y", "yes"):
            rv = True
        elif value in ("n", "no"):
            rv = False
        elif default is not None and value == "":
            rv = default
        else:
            echo("Error: invalid input", bg="yellow", fg="black", err=err)
            continue
        break
    if abort and not rv:
        raise Abort()
    return rv

##########################################################################




def evoke():
    session = Elicit()

    session.elicit
#

def terminalsize():
    """Returns the current size of the terminal as tuple in the form
    ``(width, height)`` in columns and rows.
    """
    import shutil

    if hasattr(shutil, "terminalsize"):
        return shutil.terminalsize()

    # We provide a sensible default for get_winterm_size() when being invoked
    # inside a subprocess. Without this, it would not provide a useful input.
    if get_winterm_size is not None:
        size = get_winterm_size()
        if size == (0, 0):
            return (79, 24)
        else:
            return size

    def ioctl_gwinsz(fd):
        try:
            import fcntl
            import termios

            cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
        except Exception:
            return
        return cr

    cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            try:
                cr = ioctl_gwinsz(fd)
            finally:
                os.close(fd)
        except Exception:
            pass
    if not cr or not cr[0] or not cr[1]:
        cr = (os.environ.get("LINES", 25), os.environ.get("COLUMNS", DEFAULT_COLUMNS))
    return int(cr[1]), int(cr[0])



def scrollable(text_or_generator, color=None):
    """This function takes a text and shows it via an environment specific
    pager on stdout.

    :param text_or_generator: the text to page, or alternatively, a
                              generator emitting the text to page.
    :param color: controls if the pager supports ANSI colors or not.  The
                  default is autodetection.
    """
    color = resolve_color_default(color)

    if inspect.isgeneratorfunction(text_or_generator):
        i = text_or_generator()
    elif isinstance(text_or_generator, str):
        i = [text_or_generator]
    else:
        i = iter(text_or_generator)

    # convert every element of i to a text type if necessary
    text_generator = (el if isinstance(el, str) else str(el) for el in i)

    from quo.implementation import pager

    return pager(itertools.chain(text_generator, "\n"), color)



def checknumber(string):
    """
    >>> checknumber("123.45")
    True
    >>> chenumber("123")
    True
    >>> checknumber("spam")
    False
    >>> checknumber("123e45678")
    False
    >>> checknumber("inf")
    True
    """
    if not _isconvertible(float, string):
        return False
    elif isinstance(string, (_text_type, _binary_type)) and (
        math.isinf(float(string)) or math.isnan(float(string))
    ):
        return string.lower() in ["inf", "-inf", "nan"]
    return True


def checkinteger(string, inttype=int):
    """
    >>> checkinteger("123")
    True
    >>> checkinteger("123.45")
    False
    """
    return (
        type(string) is inttype
        or (isinstance(string, _binary_type) or isinstance(string, _text_type))
        and _isconvertible(inttype, string)
    )


def checkbool(string):
    """
    >>> checkbool(True)
    True
    >>> checkbool("False")
    True
    >>> checkbool(1)
    False
    """
    return type(string) is _bool_type or (
        isinstance(string, (_binary_type, _text_type)) and string in ("True", "False")
    )



def clear():
    """Clears the terminal screen.  This will have the effect of clearing
    the whole visible space of the terminal and moving the cursor to the
    top left.  This does not do anything if not connected to a terminal.

    """
    if not isatty(sys.stdout):
        return
    # If we're on Windows and we don't have colorama available, then we
    # clear the screen by shelling out.  Otherwise we can use an escape
    # sequence.
    if WIN:
        os.system("class")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


def _interpret_color(color, offset=0):
    if isinstance(color, int):
        return f"{38 + offset};5;{color:d}"

    if isinstance(color, (tuple, list)):
        r, g, b = color
        return f"{38 + offset};2;{r:d};{g:d};{b:d}"

    return str(ansi_color_codes[color] + offset)


def style(
    text,
    fg=None,
    foreground=None,
    bg=None,
    background=None,
    bold=None,
    dim=None,
    lowercase=None,
    underline=None,
    blink=None,
    italic=None,
    reverse=None,
    reset=True,
):
    """Styles a text with ANSI styles and returns the new string.  By
    default the styling is self contained which means that at the end
    of the string a reset code is issued.  This can be prevented by
    passing ``reset=False``.

    Examples::

        quo.inscribe(quo.style('Hello World!', foreground='green'))
        quo.echo(quo.style('ATTENTION!', blink=True))
        quo.echo(quo.style('Some things', reverse=True, foreground='cyan'))
        quo.echo(quo.style('More colors', foreground=(255, 12, 128), background=117))

  Note: v as in vblack or vred stands for vivid black or vivid red
  Supported color names:

    * ``black`` (might be a gray)
    * ``red``
    * ``green``
    * ``yellow`` (might be an orange)
    * ``blue``
    * ``magenta``
    * ``cyan``
    * ``white`` (might be light gray)
    * ``vblack``
    * ``vred``
    * ``vgreen``
    * ``vyellow``
    * ``vblue``
    * ``vmagenta``
    * ``vcyan``
    * ``vwhite``
    * ``reset`` (reset the color code only)

    If the terminal supports it, color may also be specified as:

    -   An integer in the interval [0, 255]. The terminal must support
        8-bit/256-color mode.
    -   An RGB tuple of three integers in [0, 255]. The terminal must
        support 24-bit/true-color mode.

    See https://en.wikipedia.org/wiki/ANSI_color and
    https://gist.github.com/XVilka/8346728 for more information.

    :param text: the string to style with ansi codes.
    :param foreground: if provided this will become the foreground color.
    :param background: if provided this will become the background color.
    :param bold: if provided this will enable or disable bold mode.
    :param dim: if provided this will enable or disable dim mode.  This is
                badly supported.
    :param underline: if provided this will enable or disable underline.
    :param blink: if provided this will enable or disable blinking.
    :param reverse: if provided this will enable or disable inverse
                    rendering (foreground becomes background and the
                    other way round).
    :param reset: by default a reset-all code is added at the end of the
                  string which means that styles do not carry over.  This
                  can be disabled to compose styles.

    """
    if not isinstance(text, str):
        text = str(text)

    bits = []

    if fg:
        try:
            bits.append(f"\033[{_interpret_color(fg)}m")
        except KeyError:
            raise TypeError(f"Unknown color {fg!r}")

    if foreground:
        try:
            bits.append(f"\033[{_interpret_color(foreground)}m")
        except KeyError:
            raise TypeError(f"Unknown color {foreground!r}")


    if bg:
        try:
            bits.append(f"\033[{_interpret_color(bg, 10)}m")
        except KeyError:
            raise TypeError(f"Unknown color {bg!r}")
    if background:
        try:
            bits.append(f"\033[{_interpret_color(background, 10)}m")
        except KeyError:
            raise TypeError(f"Unknown color {background!r}")

    if bold is not None:
        bits.append(f"\033[{1 if bold else 22}m")
    if dim is not None:
        bits.append(f"\033[{2 if dim else 22}m")
    if underline is not None:
        bits.append(f"\033[{4 if underline else 24}m")
    if blink is not None:
        bits.append(f"\033[{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"\033[{7 if reverse else 27}m") 
    if italic is not None:
        bits.append(f"\x1B[3m")

    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return "".join(bits)


def unstyle(text):
    """Removes ANSI styling information from a string.  Usually it's not
    necessary to use this function as quo's echo function will
    automatically remove styling if necessary.

    :param text: the text to remove style information from.
    """
    return strip_ansi_colors(text)


def echo(message=None, file=None, nl=True, err=False, color=None, **styles):
    """This function combines :func:`inscribe` and :func:`style` into one
    call.  As such the following two calls are the same::

        quo.echo('Hello World!', fg='green')
        quo.inscribe(quo.style('Hello World!', fg='green'))

    All keyword arguments are forwarded to the underlying functions
    depending on which one they go with.

    Non-string types will be converted to :class:`str`. However,
    :class:`bytes` are passed directly to :meth:`inscribe` without applying
    style. If you want to style bytes that represent text, call
    :meth:`bytes.decode` first.

    """
    if message is not None and not is_bytes(message):
        message = style(message, **styles)

    return inscribe(message, file=file, nl=nl, err=err, color=color)


def edit(
    text=None, editor=None, env=None, require_save=True, extension=".txt", filename=None
):
    r"""Edits the given text in the defined editor.  If an editor is given
    (should be the full path to the executable but the regular operating
    system search path is used for finding the executable) it overrides
    the detected editor.  Optionally, some environment variables can be
    used.  If the editor is closed without changes, `None` is returned.  In
    case a file is edited directly the return value is always `None` and
    `require_save` and `extension` are ignored.

    If the editor cannot be opened a :exc:`UsageError` is raised.

    Note for Windows: to simplify cross-platform usage, the newlines are
    automatically converted from POSIX to Windows and vice versa.  As such,
    the message here will have ``\n`` as newline markers.

    :param text: the text to edit.
    :param editor: optionally the editor to use.  Defaults to automatic
                   detection.
    :param env: environment variables to forward to the editor.
    :param require_save: if this is true, then not saving in the editor
                         will make the return value become `None`.
    :param extension: the extension to tell the editor about.  This defaults
                      to `.txt` but changing this might change syntax
                      highlighting.
    :param filename: if provided it will edit this file instead of the
                     provided text contents.  It will not use a temporary
                     file as an indirection in that case.
    """
    from quo.implementation import Editor

    editor = Editor(
        editor=editor, env=env, require_save=require_save, extension=extension
    )
    if filename is None:
        return editor.edit(text)
    editor.edit_file(filename)


def launch(url, wait=False, locate=False):
    """This function launches the given URL (or filename) in the default
    viewer application for this file type.  If this is an executable, it
    might launch the executable in a new session.  The return value is
    the exit code of the launched application.  Usually, ``0`` indicates
    success.

    Examples::

        quo.launch('https://quo.readthedocs.org/')
        quo.launch('/my/downloaded/file', locate=True)

    :param url: URL or filename of the thing to launch.
    :param wait: Wait for the program to exit before returning. This
        only works if the launched program blocks. In particular,
        ``xdg-open`` on Linux does not block.
    :param locate: if this is set to `True` then instead of launching the
                   application associated with the URL it will attempt to
                   launch a file manager with the file located.  This
                   might have weird effects if the URL does not point to
                   the filesystem.
    """
    from quo.implementation import open_url

    return open_url(url, wait=wait, locate=locate)


# If this is provided, interpose() calls into this instead.  This is used
# for unittesting purposes.
_interpose = None


def interpose(inscribe=False):
    """Fetches a single character from the terminal and returns it.  This
    will always return a unicode character and under certain rare
    circumstances this might return more than one character.  The
    situations which more than one character is returned is when for
    whatever reason multiple characters end up in the terminal buffer or
    standard input was not actually a terminal.

    Note that this will always read from the terminal, even if something
    is piped into the standard input.

    Note for Windows: in rare cases when typing non-ASCII characters, this
    function might wait for a second character and then return both at once.
    This is because certain Unicode characters look like special-key markers.


    :param inscribe: if set to `True`, the character read will also show up on
                 the terminal.  The default is to not show it.
    """
    f = _interpose
    if f is None:
        from quo.implementation import interpose as f
    return f(inscribe)


def raw_terminal():
    from quo.implementation import raw_terminal as f

    return f()


def pause(info="Press any key to proceed >> ...", err=False):
    """This command stops execution and waits for the user to press any
    key to continue.  This is similar to the Windows batch "pause"
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
            echo(info, nl=False, err=err, fg="cyan")
        try:
            interpose()
        except (KeyboardInterrupt, EOFError):
            pass
    finally:
        if info:
            inscribe(err=err)

