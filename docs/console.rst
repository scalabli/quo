.. _console:

Console API
===========

For complete control over terminal formatting, Quo offers a :class:`~quo.console.Console` class. Most applications will require a single Console instance, so you may want to create one at the module level or as an attribute of your top-level object. For example, you  could add a file called "console.py" to your project::

    from quo import Console
    console = Console()

Then you can import the console from anywhere in your project like this::

    from my_file.console import console


Attributes
----------

The console will auto-detect a number of properties required when rendering.

* :obj:`~quo.Console.size` is the current dimensions of the terminal (which may change if you resize the window).
* :obj:`~quo.Console.encoding` is the default encoding (typically "utf-8").
* :obj:`~quo.Console.is_terminal` is a boolean that indicates if the Console instance is writing to a terminal or not.


Printing
--------

To write rich content to the terminal use the :meth:`~quo.Console.echo` method. Here are some examples::

    console.echo([1, 2, 3])
    console.echo("[blue underline]Looks like a link")
    console.echo(locals())
    console.echo("FOO", style="white on blue")


``Launching Editors``
-----------------------
Quo supports launching editors automatically through :func:`quo.Console.edit`.  This is very useful for asking users for multi-line input.  It will automatically open the user's defined editor or fall back to  sensible default.  If the user closes the editor without saving, the return value will be ``None``, otherwise the entered text.

**Parameters**
    - ``text`` *(str)* - The text to edit.
    - ``editor`` Optional - The editor to use.  Defaults to automatic                                    detection.
    - ``env`` *(str)*  - The environment variables to forward to the editor.
    - ``require_save`` *(bool)* - If this is true, then not saving in the editor  will make the return value become `None`.
    - ``extension`` *(str)* - The extension to tell the editor about.  This defaults to `.txt` but changing this might change syntax highlighting.
    - ``filename`` *(str)* - If provided it will edit this file instead of the provided text contents.  It will not use a temporary file as an indirection in that case.    

.. note::
    For Windows: to simplify cross-platform usage, the newlines are automatically converted from POSIX to Windows and vice versa.  As such, the message here will have ``\n`` as newline markers

.. code:: python

    from quo import Console

    console = Console()
    
    def get_commit_message():
        MARKER = '# Everything below is ignored\n'
        message = console.edit('\n\n' + MARKER)
        if message is not None:
            return message.split(MARKER, 1)[0].rstrip('\n')
           
Alternatively, the function can also be used to launch editors for files by a specific filename.  In this case, the return value is always `None`.

.. code:: python

    from quo import Console

    console = Console()
    console.edit(filename='/etc/passwd')


``File Opening``
-------------------
The logic for opening files from the :class:`quo.types.File` type is exposed through the :func:`quo.Console.openfile` function.  It can intelligently open stdin/stdout as well as any other file.
**Parameters**
    - ``filename`` *(str)* - The name of the file to open (or ``'-'`` for stdin/stdout).
    - ``mode`` *(str)* - The mode in which to open the file. 
    - ``encoding`` Optional - The encoding to use.
    - ``errors`` *(str)*  - The error handling for this file.
    - ``lazy`` *(bool)* - Can be flipped to true to open the file lazily.
    - ``atomic`` *(bool)* -in atomic mode writes go into a temporary file and it's moved on close.

.. code:: python

    from quo import Console

    console = Console()

    stdout = console.openfile('-', 'w')
    test_file = console.openfile('test.txt', 'w')

If stdin or stdout are returned, the return value is wrapped in a special file where the context manager will prevent the closing of the file.  This makes the handling of standard streams transparent and you can always use it like this:

.. code:: python

   from quo import Console

   console = Console()

   with console.openfile(filename, 'w') as f:
   f.write('Hello World!\n')

``Launching Applications``
---------------------------

Quo supports launching applications through :func:`quo.Console.launch`.  This
can be used to open the default application associated with a URL or filetype.

This can be used to launch web browsers or picture viewers, for instan
ce. In addition to this, it can also launch the file manager and automatically select the provided file.

**Parameters**
    - ``url`` *(str)* – URL or filename of the thing to launch.
    - ``wait`` *(bool)* – Wait for the program to exit before returning. This only works if the launched program blocks. In particular, xdg- open on Linux does not block.
      
    - ``locate`` Optional *(bool)* – if this is set to True then instead of launching the application associated with the URL it will attempt to launch a file manager with the file located. This might have weird effects if the URL does not point to the filesystem.


.. code:: python
   
   from quo import Console
  
   console = Console()
 
   console.launch("https://quo.rtfd.io/"

.. code:: python

   from quo import Console

   console = Console()

   console.launch("/home/downloads/file.txt", locate=True)

``Terminal size``
-----------------
Function :func:`quo.Console.size` returns the current size of the terminal as tuple in the form ``(width, height)`` in columns and rows.

.. code:: python

   from quo import Console

   console = Console()
   console.size()


``Encoding``
-------------
The default encoding of the Terminal (typically "utf-8")

.. code:: python

   from quo import Console

   console = Console()

   console.encoding()

``Rules``
----------

The :meth:`~quo.Console.rule` method will draw a horizontal bar with an optional title, which is a good way of dividing your terminal output in to sections.
provided file.

**Parameters**
      - ``message`` Optional *(str)* – Message print on the terminal



.. code:: python
   from quo import Console
   
   console = Console()

   console.rule("Chapter One")


.. image:: https://raw.githubusercontent.com/secretum-inc/quo/master/docs/images/rule.png


Status
------

Rich can display a status message with a 'spinner' animation that won't interfere with regular console output. Run the following command for a demo of this feature::

    python -m rich.status

To display a status message, call :meth:`~rich.console.Console.status` with the status message (which may be a string, Text, or other renderable). The result is a context manager which starts and stop the status display around a block of code. Here's an example::

    with console.status("Working..."):
        do_work()

You can change the spinner animation via the ``spinner`` parameter::

    with console.status("Monkeying around...", spinner="monkey"):
        do_work()

Run the following command to see the available choices for ``spinner``::

    python -m rich.spinner


Justify / Alignment
-------------------

Both print and log support a ``justify`` argument which if set must be one of "default", "left", "right", "center", or "full".  If "left", any text printed (or logged) will be left aligned, if "right" text will be aligned to the right of the terminal, if "center" the text will be centered, and if "full" the text will be lined up with both the left and right edges of the terminal (like printed text in a book). 

The default for ``justify`` is ``"default"`` which will generally look the same as ``"left"`` but with a subtle difference. Left justify will pad the right of the text with spaces, while a default justify will not. You will only notice the difference if you set a background color with the ``style`` argument. The following example demonstrates the difference::

    from rich.console import Console

    console = Console(width=20)

    style = "bold white on blue"
    console.print("Rich", style=style)
    console.print("Rich", style=style, justify="left")
    console.print("Rich", style=style, justify="center")
    console.print("Rich", style=style, justify="right")


This produces the following output:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #c0c0c0; background-color: #000080; font-weight: bold">Rich
    Rich               &nbsp;
            Rich       &nbsp; 
                    Rich
    </span></pre>

Overflow
--------

Overflow is what happens when text you print is larger than the available space. Overflow may occur if you print long 'words' such as URLs for instance, or if you have text inside a panel or table cell with restricted space.

You can specify how Rich should handle overflow with the ``overflow`` argument to  :meth:`~rich.console.Console.print` which should be one of the following strings: "fold", "crop", "ellipsis", or "ignore". The default is "fold" which will put any excess characters on the following line, creating as many new lines as required to fit the text.

The "crop" method truncates the text at the end of the line, discarding any characters that would overflow.

The "ellipsis" method is similar to "crop", but will insert an ellipsis character ("…") at the end of any text that has been truncated.

The following code demonstrates the basic overflow methods::

    from typing import List
    from rich.console import Console, OverflowMethod

    console = Console(width=14)
    supercali = "supercalifragilisticexpialidocious"

    overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(supercali, overflow=overflow, style="bold blue")
        console.print()

This produces the following output:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #00ff00">──── </span>fold<span style="color: #00ff00"> ────</span>
    <span style="color: #000080; font-weight: bold">supercalifragi
    listicexpialid
    ocious
    </span>
    <span style="color: #00ff00">──── </span>crop<span style="color: #00ff00"> ────</span>
    <span style="color: #000080; font-weight: bold">supercalifragi
    </span>
    <span style="color: #00ff00">── </span>ellipsis<span style="color: #00ff00"> ──</span>
    <span style="color: #000080; font-weight: bold">supercalifrag…
    </span>
    </pre>

You can also set overflow to "ignore" which allows text to run on to the next line. In practice this will look the same as "crop" unless you also set ``crop=False`` when calling :meth:`~rich.console.Console.print`.


Console style
-------------

The Console has a ``style`` attribute which you can use to apply a style to everything you print. By default ``style`` is None meaning no extra style is applied, but you can set it to any valid style. Here's an example of a Console with a style attribute set::

    from rich.console import Console
    blue_console = Console(style="white on blue")
    blue_console.print("I'm blue. Da ba dee da ba di.")


Soft Wrapping
-------------

Rich word wraps text you print by inserting line breaks. You can disable this behavior by setting ``soft_wrap=True`` when calling :meth:`~rich.console.Console.print`. With *soft wrapping* enabled any text that doesn't fit will run on to the following line(s), just like the builtin ``print``.


Cropping
--------

The :meth:`~rich.console.Console.print` method has a boolean ``crop`` argument. The default value for crop is True which tells Rich to crop any content that would otherwise run on to the next line. You generally don't need to think about cropping, as Rich will resize content to fit within the available width.

.. note::
    Cropping is automatically disabled if you print with ``soft_wrap=True``.


Input
-----

The console class has an :meth:`~rich.console.Console.input` method which works in the same way as Python's builtin :func:`input` function, but can use anything that Rich can print as a prompt. For example, here's a colorful prompt with an emoji::

    from rich.console import Console
    console = Console()
    console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")

If Python's builtin :mod:`readline` module is previously loaded, elaborate line editing and history features will be available.

Exporting
---------

The Console class can export anything written to it as either text or html. To enable exporting, first set ``record=True`` on the constructor. This tells Rich to save a copy of any data you ``print()`` or ``log()``. Here's an example::

    from rich.console import Console
    console = Console(record=True)

After you have written content, you can call :meth:`~rich.console.Console.export_text` or :meth:`~rich.console.Console.export_html` to get the console output as a string. You can also call :meth:`~rich.console.Console.save_text` or :meth:`~rich.console.Console.save_html` to write the contents directly to disk.

For examples of the html output generated by Rich Console, see :ref:`appendix-colors`.

Error console
-------------

The Console object will write to ``sys.stdout`` by default (so that you see output in the terminal). If you construct the Console with ``stderr=True`` Rich will write to ``sys.stderr``. You may want to use this to create an *error console* so you can split error messages from regular output. Here's an example::

    from rich.console import Console    
    error_console = Console(stderr=True)

You might also want to set the ``style`` parameter on the Console to make error messages visually distinct. Here's how you might do that::

    error_console = Console(stderr=True, style="bold red")

File output
-----------

You can also tell the Console object to write to a file by setting the ``file`` argument on the constructor -- which should be a file-like object opened for writing text. You could use this to write to a file without the output ever appearing on the terminal. Here's an example::

    import sys
    from rich.console import Console
    from datetime import datetime

    with open("report.txt", "wt") as report_file:
        console = Console(file=report_file)
        console.rule(f"Report Generated {datetime.now().ctime()}")
        
Note that when writing to a file you may want to explicitly the ``width`` argument if you don't want to wrap the output to the current console width.

Capturing output
----------------

There may be situations where you want to *capture* the output from a Console rather than writing it directly to the terminal. You can do this with the :meth:`~rich.console.Console.capture` method which returns a context manager. On exit from this context manager, call :meth:`~rich.console.Capture.get` to return the string that would have been written to the terminal. Here's an example::

    from rich.console import Console
    console = Console()
    with console.capture() as capture:
        console.print("[bold red]Hello[/] World")
    str_output = capture.get()

An alternative way of capturing output is to set the Console file to a :py:class:`io.StringIO`. This is the recommended method if you are testing console output in unit tests. Here's an example::

    from io import StringIO
    from rich.console import Console
    console = Console(file=StringIO())
    console.print("[bold red]Hello[/] World")
    str_output = console.file.getvalue()

Paging
------

If you have some long output to present to the user you can use a *pager* to display it. A pager is typically an application on your operating system which will at least support pressing a key to scroll, but will often support scrolling up and down through the text and other features.

You can page output from a Console by calling :meth:`~rich.console.Console.pager` which returns a context manager. When the pager exits, anything that was printed will be sent to the pager. Here's an example::

    from rich.__main__ import make_test_card
    from rich.console import Console

    console = Console()
    with console.pager():
        console.print(make_test_card())

Since the default pager on most platforms don't support color, Rich will strip color from the output. If you know that your pager supports color, you can set ``styles=True`` when calling the :meth:`~rich.console.Console.pager` method.

.. note::
    Rich will use the ``PAGER`` environment variable to get the pager command. On Linux and macOS you can set this to ``less -r`` to enable paging with ANSI styles.

Alternate screen
----------------

.. warning::
    This feature is currently experimental. You might want to wait before using it in production.

Terminals support an 'alternate screen' mode which is separate from the regular terminal and allows for full-screen applications that leave your stream of input and commands intact. Rich supports this mode via the :meth:`~rich.console.Console.set_alt_screen` method, although it is recommended that you use :meth:`~rich.console.Console.screen` which returns a context manager that disables alternate mode on exit.

Here's an example of an alternate screen::

    from time import sleep
    from rich.console import Console

    console = Console()
    with console.screen():
        console.print(locals())
        sleep(5)
        
The above code will display a pretty printed dictionary on the alternate screen before returning to the command prompt after 5 seconds.

You can also provide a renderable to :meth:`~rich.console.Console.screen` which will be displayed in the alternate screen when you call :meth:`~rich.ScreenContext.update`. 

Here's an example::

    from time import sleep

    from rich.console import Console
    from rich.align import Align
    from rich.text import Text
    from rich.panel import Panel

    console = Console()

    with console.screen(style="bold white on red") as screen:
        for count in range(5, 0, -1):
            text = Align.center(
                Text.from_markup(f"[blink]Don't Panic![/blink]\n{count}", justify="center"),
                vertical="middle",
            )
            screen.update(Panel(text))
            sleep(1)

Updating the screen with a renderable allows Rich to crop the contents to fit the screen without scrolling.

For a more powerful way of building full screen interfaces with Rich, see :ref:`live`.


.. note::
    If you ever find yourself stuck in alternate mode after exiting Python code, type ``reset`` in the terminal

Terminal detection
------------------

If Rich detects that it is not writing to a terminal it will strip control codes from the output. If you want to write control codes to a regular file then set ``force_terminal=True`` on the constructor.

Letting Rich auto-detect terminals is useful as it will write plain text when you pipe output to a file or other application.

Interactive mode
~~~~~~~~~~~~~~~~

Rich will remove animations such as progress bars and status indicators when not writing to a terminal as you probably don't want to write these out to a text file (for example). You can override this behavior by setting the ``force_interactive`` argument on the constructor. Set it to True to enable animations or False to disable them.

.. note::
    Some CI systems support ANSI color and style but not anything that moves the cursor or selectively refreshes parts of the terminal. For these you might want to set ``force_terminal`` to ``True`` and ``force_interactive`` to ``False``.

Environment variables
---------------------

Rich respects some standard environment variables.

Setting the environment variable ``TERM`` to ``"dumb"`` or ``"unknown"`` will disable color/style and some features that require moving the cursor, such as progress bars.

If the environment variable ``NO_COLOR`` is set, Rich will disable all color in the output.

``A simple console application``
---------------------------------

Almost every quo application is an instance of an :class:`~quo.Console` object. The simplest full screen example would look like this:
.. code:: python

    from quo import Console
    
    Console(full_screen=True).run()

This will display an application with no layout specified.
.. note::

        If we wouldn't set the ``full_screen`` option, the application would not run in the alternate screen buffer, and only consume the least amount of space required for the layout.

:ref:`Read more about full-screen console applications ...<full_screen_app>`
