#This module contains implementations for the module
#Some infrequently used functionality are
#placed in this module and only imported as needed.

import contextlib
import math
import os
import sys
import time

from .accordance import _default_text_stdout
from .accordance import CYGWIN
from .accordance import default_system_encoding
from .accordance import isatty
from .accordance import openstream
from .accordance import strip_ansi_colors
from .accordance import term_len
from .accordance import WIN
from quo.outliers.exceptions import QuoException
from quo.expediency import inscribe
from quo.i_o import echo

if os.name == "nt":
    BEFORE_BAR = "\r"
    AFTER_BAR = "\n"
else:
    BEFORE_BAR = "\r\033[?25l"
    AFTER_BAR = "\033[?25h\n"


def _length_hint(obj):
    """Returns the length hint of an object."""
    try:
        return len(obj)
    except (AttributeError, TypeError):
        try:
            get_hint = type(obj).__length_hint__
        except AttributeError:
            return None
        try:
            hint = get_hint(obj)
        except TypeError:
            return None
        if hint is NotImplemented or not isinstance(hint, int) or hint < 0:
            return None
        return hint
################################################################



################################################################

def scrollable(generator, color=None):
    """Decide what method to use for paging through text."""
    stdout = _default_text_stdout()
    if not isatty(sys.stdin) or not isatty(stdout):
        return _nullpager(stdout, generator, color)
    pager_cmd = (os.environ.get("PAGER", None) or "").strip()
    if pager_cmd:
        if WIN:
            return _tempfilepager(generator, pager_cmd, color)
        return _pipepager(generator, pager_cmd, color)
    if os.environ.get("TERM") in ("dumb", "emacs"):
        return _nullpager(stdout, generator, color)
    if WIN or sys.platform.startswith("os2"):
        return _tempfilepager(generator, "more <", color)
    if hasattr(os, "system") and os.system("(less) 2>/dev/null") == 0:
        return _pipepager(generator, "less", color)

    import tempfile

    fd, filename = tempfile.mkstemp()
    os.close(fd)
    try:
        if hasattr(os, "system") and os.system(f'more "{filename}"') == 0:
            return _pipepager(generator, "more", color)
        return _nullpager(stdout, generator, color)
    finally:
        os.unlink(filename)


def _pipepager(generator, cmd, color):
    """Page through text by feeding it to another program.  Invoking a
    pager through this might support colors.
    """
    import subprocess

    env = dict(os.environ)

    # If we're piping to less we might support colors under the
    # condition that
    cmd_detail = cmd.rsplit("/", 1)[-1].split()
    if color is None and cmd_detail[0] == "less":
        less_flags = f"{os.environ.get('LESS', '')}{' '.join(cmd_detail[1:])}"
        if not less_flags:
            env["LESS"] = "-R"
            color = True
        elif "r" in less_flags or "R" in less_flags:
            color = True

    c = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, env=env)
    encoding = get_best_encoding(c.stdin)
    try:
        for text in generator:
            if not color:
                text = strip_ansi_colors(text)

            c.stdin.write(text.encode(encoding, "replace"))
    except (OSError, KeyboardInterrupt):
        pass
    else:
        c.stdin.close()

    # Less doesn't respect ^C, but catches it for its own UI purposes (aborting
    # search or other commands inside less).
    #
    # That means when the user hits ^C, the parent process (Quo) terminates,
    # but less is still alive, paging the output and messing up the terminal.
    #
    # If the user wants to make the pager exit on ^C, they should set
    # `LESS='-K'`. It's not our decision to make.
    while True:
        try:
            c.wait()
        except KeyboardInterrupt:
            pass
        else:
            break


def _tempfilepager(generator, cmd, color):
    """Page through text by invoking a program on a temporary file."""
    import tempfile

    filename = tempfile.mktemp()
    # TODO: This never terminates if the passed generator never terminates.
    text = "".join(generator)
    if not color:
        text = strip_ansi_colors(text)
    encoding = get_best_encoding(sys.stdout)
    with open_stream(filename, "wb")[0] as f:
        f.write(text.encode(encoding))
    try:
        os.system(f'{cmd} "{filename}"')
    finally:
        os.unlink(filename)


def _nullpager(stream, generator, color):
    """Simply print unformatted text.  This is the ultimate fallback."""
    for text in generator:
        if not color:
            text = strip_ansi_colors(text)
        stream.write(text)


class Editor:
    def __init__(self, editor=None, env=None, require_save=True, extension=".txt"):
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension

    def get_editor(self):
        if self.editor is not None:
            return self.editor
        for key in "VISUAL", "EDITOR":
            rv = os.environ.get(key)
            if rv:
                return rv
        if WIN:
            return "notepad"
        for editor in "sensible-editor", "vim", "nano":
            if os.system(f"which {editor} >/dev/null 2>&1") == 0:
                return editor
        return "vi"

    def edit_file(self, filename):
        import subprocess

        editor = self.get_editor()
        if self.env:
            environ = os.environ.copy()
            environ.update(self.env)
        else:
            environ = None
        try:
            c = subprocess.Popen(f'{editor} "{filename}"', env=environ, shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise QuoException(f"{editor}: Editing failed!")
        except OSError as e:
            raise QuoException(f"{editor}: Editing failed: {e}")

    def edit(self, text):
        import tempfile

        if not text:
            text = ""

        is_bytes = isinstance(text, (bytes, bytearray))

        if not is_bytes:
            if text and not text.endswith("\n"):
                text += "\n"

            if WIN:
                text = text.replace("\n", "\r\n").encode("utf-8-sig")
            else:
                text = text.encode("utf-8")

        fd, name = tempfile.mkstemp(prefix="editor-", suffix=self.extension)

        try:
            with os.fdopen(fd, "wb") as f:
                f.write(text)

            # If the filesystem resolution is 1 second, like Mac OS
            # 10.12 Extended, or 2 seconds, like FAT32, and the editor
            # closes very fast, require_save can fail. Set the modified
            # time to be 2 seconds in the past to work around this.
            os.utime(name, (os.path.getatime(name), os.path.getmtime(name) - 2))
            # Depending on the resolution, the exact value might not be
            # recorded, so get the new recorded value.
            timestamp = os.path.getmtime(name)

            self.edit_file(name)

            if self.require_save and os.path.getmtime(name) == timestamp:
                return None

            with open(name, "rb") as f:
                rv = f.read()

            if is_bytes:
                return rv

            return rv.decode("utf-8-sig").replace("\r\n", "\n")
        finally:
            os.unlink(name)


def open_url(url, wait=False, locate=False):
    import subprocess

    def _unquote_file(url):
        import urllib

        if url.startswith("file://"):
            url = urllib.unquote(url[7:])
        return url

    if sys.platform == "darwin":
        args = ["open"]
        if wait:
            args.append("-W")
        if locate:
            args.append("-R")
        args.append(_unquote_file(url))
        null = open("/dev/null", "w")
        try:
            return subprocess.Popen(args, stderr=null).wait()
        finally:
            null.close()
    elif WIN:
        if locate:
            url = _unquote_file(url.replace('"', ""))
            args = f'explorer /select,"{url}"'
        else:
            url = url.replace('"', "")
            wait = "/WAIT" if wait else ""
            args = f'start {wait} "" "{url}"'
        return os.system(args)
    elif CYGWIN:
        if locate:
            url = os.path.dirname(_unquote_file(url).replace('"', ""))
            args = f'cygstart "{url}"'
        else:
            url = url.replace('"', "")
            wait = "-w" if wait else ""
            args = f'cygstart {wait} "{url}"'
        return os.system(args)

    try:
        if locate:
            url = os.path.dirname(_unquote_file(url)) or "."
        else:
            url = _unquote_file(url)
        c = subprocess.Popen(["xdg-open", url])
        if wait:
            return c.wait()
        return 0
    except OSError:
        if url.startswith(("http://", "https://")) and not locate and not wait:
            import webbrowser

            webbrowser.open(url)
            return 0
        return 1


def _translate_ch_to_exc(ch):
    if ch == "\x03":
        raise KeyboardInterrupt()
    if ch == "\x04" and not WIN:  # Unix-like, Ctrl+D
        raise EOFError()
    if ch == "\x1a" and WIN:  # Windows, Ctrl+Z
        raise EOFError()


if WIN:
    import msvcrt

    @contextlib.contextmanager
    def raw_terminal():
        yield

    def interpose (echo):
        # The function `getch` will return a bytes object corresponding to
        # the pressed character. Since Windows 10 build 1803, it will also
        # return \x00 when called a second time after pressing a regular key.
        #
        # `getwch` does not share this probably-bugged behavior. Moreover, it
        # returns a Unicode object by default, which is what we want.
        #
        # Either of these functions will return \x00 or \xe0 to indicate
        # a special key, and you need to call the same function again to get
        # the "rest" of the code. The fun part is that \u00e0 is
        # "latin small letter a with grave", so if you type that on a French
        # keyboard, you _also_ get a \xe0.
        # E.g., consider the Up arrow. This returns \xe0 and then \x48. The
        # resulting Unicode string reads as "a with grave" + "capital H".
        # This is indistinguishable from when the user actually types
        # "a with grave" and then "capital H".
        #
        # When \xe0 is returned, we assume it's part of a special-key sequence
        # and call `getwch` again, but that means that when the user types
        # the \u00e0 character, `interpose ` doesn't return until a second
        # character is typed.
        # The alternative is returning immediately, but that would mess up
        # cross-platform handling of arrow keys and others that start with
        # \xe0. Another option is using `getch`, but then we can't reliably
        # read non-ASCII characters, because return values of `getch` are
        # limited to the current 8-bit codepage.
        #
        # Anyway, Quo doesn't claim to do this Right(tm), and using `getwch`
        # is doing the right thing in more situations than with `getch`.
        if echo:
            func = msvcrt.getwche
        else:
            func = msvcrt.getwch

        rv = func()
        if rv in ("\x00", "\xe0"):
            # \x00 and \xe0 are control characters that indicate special key,
            # see above.
            rv += func()
        _translate_ch_to_exc(rv)
        return rv


else:
    import tty
    import termios

    @contextlib.contextmanager
    def raw_terminal():
        if not isatty(sys.stdin):
            f = open("/dev/tty")
            fd = f.fileno()
        else:
            fd = sys.stdin.fileno()
            f = None
        try:
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                yield fd
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                sys.stdout.flush()
                if f is not None:
                    f.close()
        except termios.error:
            pass

    def interpose (echo):
        with raw_terminal() as fd:
            ch = os.read(fd, 32)
            ch = ch.decode(default_system_encoding(sys.stdin), "replace")
            if echo and isatty(sys.stdout):
                sys.stdout.write(ch)
            _translate_ch_to_exc(ch)
            return ch
