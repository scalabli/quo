Utilities
=========

.. currentmodule:: quo

Besides the functionality that quo provides to interface with argument
parsing and handling, it also provides a bunch of addon functionality that
is useful for writing command line utilities.


Printing to Stdout
------------------

The most obvious helper is the :func:`echo` function, which in many ways
works like the Python ``print`` statement or function.  The main difference is
that it works the same in many different terminal environments.

Example:

.. code:: python

    import quo
    quo.echo('Hello World!')

It can output both text and binary data. It will emit a trailing newline
by default, which needs to be suppressed by passing ``nl=False``:

.. code:: python

   import quo
   quo.echo(b'\xe2\x98\x83', nl=False)

Last but not least :func:`echo` uses quo's intelligent internal output
streams to stdout and stderr which support unicode output on the Windows
console.  This means for as long as you are using `quo.echo` you can
output unicode characters (there are some limitations on the default font
with regards to which characters can be displayed).

Quo emulates output streams on Windows to support unicode to the
Windows console through separate APIs.  For more information see
:doc:`wincmd`.

Printing to Standard error
---------------------------
You can easily print to standard error by passing ``err=True``:

.. code:: python

   import quo
   quo.echo('Hello World!', err=True)


.. _ansi-colors:

American National Standards Institute(ANSI) Colors
-----------

The :func:`echo` function gained extra functionality to deal with ANSI
colors and styles.  Note that on Windows, this functionality is only
available if `colorama`_ is installed.  If it is installed, then ANSI
codes are intelligently handled.

Primarily this means that:

-   Quo's :func:`echo` function will automatically strip ANSI color codes
    if the stream is not connected to a terminal.
-   the :func:`echo` function will transparently connect to the terminal on
    Windows and translate ANSI codes to terminal API calls.  This means
    that colors will work on Windows the same way they do on other
    operating systems.

Note for `colorama` support: Quo will automatically detect when `colorama`
is available and use it.  Do *not* call ``colorama.init()``!

To install `colorama`, run this command::

    $ pip install colorama

For styling and adding more flair to  a string, :meth: fg or :meth: bg; amongst others, can be attached to the :func:`echo` :

.. code:: python

    import quo
    from quo import echo
    echo('Hello World!', fg='green')
    echo('Some more text', bg='blue', fg='white')
    echo('ATTENTION', blink= True, bold= True, italic= True)

.. _colorama: https://pypi.org/project/colorama/

Scrollable test
-------------

In some situations, you might want to show long texts on the terminal and
let a user scroll through it.  This can be achieved by using the
:func:`scrollable` function which works similarly to the :func:`echo`
function, but always writes to stdout.

Example::

    @quo.command()
    def less():
        quo.scrollable("\n".join(f"Line {idx}" for idx in range(200)))

If you want to print a lot of text, especially if generating everything in advance would take a lot of time, you can pass a generator (or generator function) instead of a string::

    def _generate_output():
        for idx in range(50000):
            yield f"Line {idx}\n"

    @quo.command()
    def less():
        quo.scrollable(_generate_output())


Screen Clearing
---------------

To clear the terminal screen, you can use the :func:`clear` function. It does what the name suggests: it
clears the entire visible screen in a platform-agnostic way:

.. code:: python

    import quo
    from quo import clear
    clear()


Getting Characters from Terminal
--------------------------------

Normally, when reading input from the terminal, you would read from
standard input.  However, this is buffered input and will not show up until
the line has been terminated.  In certain circumstances, you might not want
to do that and instead read individual characters as they are being written.

For this, Quo provides the :func:`interpose` function which reads a single
character from the terminal buffer and returns it as a Unicode character.

Note that this function will always read from the terminal, even if stdin
is instead a pipe.

.. code:: python

    import quo
    from quo import echo, interpose, confirm
    confirm(f"Start Interpose")
    c = interpose()
    quo.echo()
    if c == 'y':
        echo('We will go on')
    elif c == 'n':
        echo('Abort!')
    else:
        echo('Invalid input :(')

Note that this reads raw input, which means that things like arrow keys
will show up in the platform's native escape format.  The only characters
translated are ``^C`` and ``^D`` which are converted into keyboard
interrupts and end of file exceptions respectively.  This is done because
otherwise, it's too easy to forget about that and to create scripts that
cannot be properly exited.


Waiting for Key Press
---------------------

Sometimes, it's useful to pause until the user presses any key on the
keyboard.  This is especially useful on Windows where ``cmd.exe`` will
close the window at the end of the command execution by default, instead
of waiting.

In quo, this can be accomplished with the :func:`pause` function.  This
function will print a quick message to the terminal (which can be
customized) and wait for the user to press a key.  In addition to that,
it will also become a NOP (no operation instruction) if the script is not
run interactively.

.. code:: python

    import quo
    from quo import pause
    pause()


Launching Editors
-----------------

Quo supports launching editors automatically through :func:`edit`.  This
is very useful for asking users for multi-line input.  It will
automatically open the user's defined editor or fall back to a sensible
default.  If the user closes the editor without saving, the return value
will be ``None``, otherwise the entered text.

.. code:: python

    import quo
    from quo import edit
    def get_commit_message():
        MARKER = '# Everything below is ignored\n'
        message = edit('\n\n' + MARKER)
        if message is not None:
            return message.split(MARKER, 1)[0].rstrip('\n')

Alternatively, the function can also be used to launch editors for files by a specific filename.  In this case, the return value is always `None`.

.. code:: python

    import quo
    from quo import edit
    edit(filename='/etc/passwd')


Launching Applications
----------------------

Quo supports launching applications through :func:`launch`.  This can be
used to open the default application associated with a URL or filetype.
This can be used to launch web browsers or picture viewers, for instance.
In addition to this, it can also launch the file manager and automatically
select the provided file.

.. code:: python
  
   import quo
   from quo import launch
   launch("https://quo.rtfd.io/")
   launch("/home/downloads/file.txt", locate=True)


Printing Filenames
------------------

Because filenames might not be Unicode, formatting them can be a bit
tricky.

The way this works with quo is through the :func:`formatfilename`
function.  It does a best-effort conversion of the filename to Unicode and
will never fail.  This makes it possible to use these filenames in the
context of a full Unicode string.

.. code:: python

   import quo
   from quo import echo, formatfilename
   echo(f"Path: {formatfilename(b'foo.txt')}")


Standard Streams
----------------

For command line utilities, it's very important to get access to input and
output streams reliably.  Python generally provides access to these
streams through ``sys.stdout`` and friends, but unfortunately, there are
API differences between 2.x and 3.x, especially with regards to how these
streams respond to Unicode and binary data.

Because of this, quo provides the :func:`binarystream` and
:func:`textstream` functions, which produce consistent results with
different Python versions and for a wide variety of terminal configurations.

The end result is that these functions will always return a functional
stream object (except in very odd cases; see :doc:`/unicode-support`).

.. code:: python

    import quo
    from quo import textstream, binarystream
    stdin_t = textstream('stdin')
    stdout_b = binarystream('stdout')

Quo now emulates output streams on Windows to support unicode to the
Windows console through separate APIs.  For more information see
:doc:`wincmd`.


Intelligent File Opening
------------------------

The logic for opening files from the :class:`File`
type is exposed through the :func:`openfile` function.  It can
intelligently open stdin/stdout as well as any other file.

.. code:: python

    import quo
    from quo openfile

    stdout = openfile('-', 'w')
    test_file = openfile('test.txt', 'w')

If stdin or stdout are returned, the return value is wrapped in a special
file where the context manager will prevent the closing of the file.  This
makes the handling of standard streams transparent and you can always use
it like this:

.. code:: python

   from quo import openfile
   with openfile(filename, 'w') as f:
   f.write('Hello World!\n')


Finding Application Folders
---------------------------

Very often, you want to open a configuration file that belongs to your
application.  However, different operating systems store these configuration
files in different locations depending on their standards.  Quo provides
a :func:`appdir` function which returns the most appropriate location
for per-user config files for your application depending on the OS.

.. code:: python

    import os
    import quo
    from quo import appdir
    import ConfigParser

    APP_NAME = 'My Application'

    def read_config():
        cfg = os.path.join(appdir(APP_NAME), 'config.ini')
        parser = ConfigParser.RawConfigParser()
        parser.read([cfg])
        rv = {}
        for section in parser.sections():
            for key, value in parser.items(section):
                rv[f"{section}.{key}"] = value
        return rv

Display tabular data
---------------------

Checking if a character is a bool
-----------------------------------



Checking if a character is a number
-------------------------------------


Checking if a character is a integer
-------------------------------------
