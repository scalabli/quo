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



``A simple console application``
---------------------------------

Almost every quo application is an instance of an :class:`~quo.Console` object.
The simplest full screen example would look like this:

.. code:: python

  from quo import Console
 
  Console(full_screen=True).run()

This will display an application with no layout specified

.. note::

        If we wouldn't set the ``full_screen`` option, the application would not run in the alternate screen buffer, and only consume the least amount of space required for the layout.

:ref:`Read more about full-screen console applications ...<full_screen_app>`
