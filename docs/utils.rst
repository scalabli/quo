Utilities
===============

``Scrollable test``
-------------------

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


``Screen Clearing``
--------------------
To clear the terminal screen, you can use the :func:`quo.clear` function. It does what the name suggests: it clears the entire visible screen in a platform-agnostic way:

.. code:: python

    from quo import clear

    clear()


``Getting Characters from Terminal(getchar)``
----------------------------------------------

Normally, when reading input from the terminal, you would read from
standard input.  However, this is buffered input and will not show up until
the line has been terminated.  In certain circumstances, you might not want
to do that and instead read individual characters as they are being written.

For this, Quo provides the :func:`getchar` function which reads a single
character from the terminal buffer and returns it as a Unicode character.

Note that this function will always read from the terminal, even if stdin
is instead a pipe.

.. code:: python

    from quo import echo, getchar
    
    gc = getchar()

    if gc == 'y':
        echo('We will go on')
    elif gc == 'n':
        echo('Abort!')
 

Note that this reads raw input, which means that things like arrow keys
will show up in the platform's native escape format.  The only characters
translated are ``^C`` and ``^D`` which are converted into keyboard
interrupts and end of file exceptions respectively.  This is done because
otherwise, it's too easy to forget about that and to create scripts that
cannot be properly exited.

``Exitting``
------------
Quo has a low-level exit that skips Python's cleanup and speeds up exit by about 10ms for things like shell completion.
**Parmameters**
     - ``code`` - Exit code.

.. code:: python

 from quo import exit

 exit(1)



``Waiting for Key Press(pause)``
--------------------------------

Sometimes, it's useful to pause until the user presses any key on the
keyboard.

In quo, this can be accomplished with the :func:`quo.pause` function.  This
function will print a quick message to the terminal (which can be
customized) and wait for the user to press a key.  In addition to that,
it will also become a NOP (no operation instruction) if the script is not
run interactively.

**Parameters**
    - ``info`` *(Optional[str])* – The message to print before pausing. Defaults to "Press any key to proceed >> ..".


.. code:: python

    from quo import pause
    
    pause()


``Printing Filenames``
-----------------------

Because filenames might not be Unicode, formatting them can be a bit
tricky.

The way this works with quo is through the :func:`quo.formatfilename`
function.  It does a best-effort conversion of the filename to Unicode and
will never fail.  This makes it possible to use these filenames in the
context of a full Unicode string.

.. code:: python

   import quo

   quo.echo(f"Path: {quo.formatfilename(b'foo.txt')}")


``Standard Streams``
---------------------

For command line utilities, it's very important to get access to input and
output streams reliably.  Python generally provides access to these
streams through ``sys.stdout`` and friends but quo provides the :func:`binarystream` and
:func:`textstream` functions, which produce consistent results with
different Python versions and for a wide variety of terminal configurations.

The end result is that these functions will always return a functional
stream object (except in very odd cases; see :doc:`/unicode-support`).

.. code:: python

    import quo

    stdin_t = quo.textstream('stdin')
    stdout_b = quo.binarystream('stdout')



``Finding Application Folders``
---------------------------------

Very often, you want to open a configuration file that belongs to your
application.  However, different operating systems store these configuration
files in different locations depending on their standards.  Quo provides
a :func:`quo.appdir` function which returns the most appropriate location
for per-user config files for your application depending on the OS.

.. code:: python

    import os
    import quo
    import ConfigParser

    APP_NAME = 'My Application'

    def read_config():
        cfg = os.path.join(quo.appdir(APP_NAME), 'config.ini')
        parser = ConfigParser.RawConfigParser()
        parser.read([cfg])
        rv = {}
        for section in parser.sections():
            for key, value in parser.items(section):
                rv[f"{section}.{key}"] = value
        return rv

