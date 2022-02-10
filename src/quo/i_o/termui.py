import inspect
import io
import itertools
import os
import struct
import sys
import math
from typing import Any, Optional, IO
from quo.accordance import (
        DEFAULT_COLUMNS,
        get_winterm_size,
        bit_bytes,
        isatty,
        strip_ansi_colors,
        )
from quo.color import ansi_color_codes, _ansi_reset_all
from quo.errors import Abort
from quo.context.current import resolve_color_default
from quo.types import Choice # convert_type
from quo.expediency import LazyFile, inscribe
#convert_type


# The prompt functions to use.  The doc tools currently override these
# functions to customize how they work.

#insert = input



def hidden_prompt_func(prompt):
    import getpass

    return getpass.getpass(prompt)


def _build_prompt(
        text, 
        suffix, 
        show_default=False,
        default=None,
        show_choices=True,
        type=None
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


#############################


##########################################################################


def confirm(
        text: Optional[str],
        default: bool = False, 
        abort: bool = False,
        suffix=":>", 
        show_default=True, 
        err=False
        ):
    """Prompts for confirmation (yes/no question).

    If the user aborts the input by sending a interrupt signal this
    function will catch it and raise a :exc:`Abort` exception.

    :param text: the question to ask.
    :param default: the default for the prompt.
    :param abort: if this is set to `True` a negative answer aborts the
                  exception by raising :exc:`Abort`.
    :param suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of
                ``stdout``, the same as with echo.
    """
    prompt = _build_prompt(
        text, suffix, show_default, "Yes/no" if default else "yes/No"
    )
    while 1:
        try:
            echo(prompt, nl=False, err=err)
            insert = input
            value = insert("").lower().strip()
        except (KeyboardInterrupt, EOFError):
            raise Abort()
        if value in ("y", "yes"):
            rv = True
        elif value in ("n", "no"):
            rv = False
        elif default is not None and value == "":
            rv = default
        else:
            echo(f"ERROR:", bg="red", fg="black", nl=False)
            echo(" ", nl=False)
            echo(f"invalid input", bg="yellow", fg="black", err=err)
            continue
        break
    if abort and not rv:
        raise Abort()
    return rv
############
########################################################



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

    from quo.implementation import scrollable

    return scrollable(itertools.chain(text_generator, "\n"), color)



def _interpret_color(color, offset=0):
    if isinstance(color, int):
        return f"{38 + offset};5;{color:d}"

    if isinstance(color, (tuple, list)):
        r, g, b = color
        return f"{38 + offset};2;{r:d};{g:d};{b:d}"

    return str(ansi_color_codes[color] + offset)


def flair(
    text,
    fg=None,
    foreground=None,
    bg=None,
    background=None,
    bold=None,
    dim=None,
    hidden=None,
    ul=None,
    underline=None,
    blink=None,
    italic=None,
    reverse=None,
    reset=True,
    strike=None,
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

    if ul is not None:
        bits.append(f"\033[{4 if ul else 24}m")
    if underline is not None:
        bits.append(f"\033[{4 if underline else 24}m")
    if blink is not None:
        bits.append(f"\033[{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"\033[{7 if reverse else 27}m") 
    if italic is not None:
        bits.append(f"\x1B[3m")
    if hidden is not None:
        bits.append(f"\x1b[8m")
    if strike is not None:
        bits.append(f"\x1b[9m")

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


def edit(
        text=None, 
        editor=None, 
        env=None, 
        require_save=True, 
        extension=".txt", 
        filename=None
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


def raw_terminal():
    from quo.implementation import raw_terminal as f
    return f()


def echo(
        message: Optional[str] = None,
        file: Optional[IO[str]] = None,
        nl: bool = True,
        err: bool = False,
        color=None,
        **styles
        ):
        """
        quo.echo('Hello World!', fg='green')
        quo.inscribe(quo.style('Hello World!', fg='green'))
        All keyword arguments are forwarded to the underlying functions  depending on which one they go with.
        Non-string types will be converted to :class:`str`. However,
        :class:`bytes` are passed directly to :meth:`inscribe` without applying
        style. If you want to style bytes that represent text, call
        :meth:`bytes.decode` first.
        """
        if message is not None and not bit_bytes(message):
            message = flair(message, **styles)

        return inscribe(message, file=file, nl=nl, err=err, color=color)


