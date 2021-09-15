Introduction
============
Quo is a Python based toolkit for writing Command-Line Interface(CLI) applications. Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API. Simple to code, easy to learn, and does not come with needless baggage.


Requirements
------------

Quo works flawlessly with Linux, OSX and Windows.

Quo requires Python ``3.6.1`` or later

.. note::
    PyCharm users will need to enable "emulate terminal" in output console option in run/debug configuration to see styled output.

Installation
------------

You can install Quo from PyPi with `pip`

.. code-block:: console

    pip install -U quo

If you intend to use Rich with Jupyter then there are some additional dependencies which you can install with the following command::

    pip install rich[jupyter]


Quick Start
-----------
.. code-block:: python

    from quo import echo

    echo(f"Hello World!", fg="red", italic=True, bold=True)

This will print ``"Hello World!"`` plus a new line to the terminal. Unlike the builtin print function, echo function has improved support for handling Unicode and binary data. If colorama is installed, the echo function will also support handling of ANSI color sequences.



This writes the following output to the terminal (including all the colors and styles):

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; font-style: italic">Hello</span> World!                                                 
    <span style="font-weight: bold">{</span>
        <span style="color: #008000">'__annotations__'</span>: <span style="font-weight: bold">{}</span>,
        <span style="color: #008000">'__builtins__'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">module</span><span style="color: #000000"> </span><span style="color: #008000">'builtins'</span><span style="color: #000000"> </span><span style="color: #000000; font-weight: bold">(</span><span style="color: #000000">built-in</span><span style="color: #000000; font-weight: bold">)</span><span style="font-weight: bold">></span>,
        <span style="color: #008000">'__doc__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'__loader__'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">class</span><span style="color: #000000"> </span><span style="color: #008000">'_frozen_importlib.BuiltinImporter'</span><span style="font-weight: bold">></span>,
        <span style="color: #008000">'__name__'</span>: <span style="color: #008000">'__main__'</span>,
        <span style="color: #008000">'__package__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'__spec__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'print'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">function</span><span style="color: #000000"> print at </span><span style="color: #000080; font-weight: bold">0x1027fd4c0</span><span style="font-weight: bold">></span>,
    <span style="font-weight: bold">}</span> </pre>


If you would rather not shadow Python's builtin print, you can import ``rich.print`` as ``rprint`` (for example)::

    from rich import print as rprint

Continue reading to learn about the more advanced features of Rich.

Rich in the REPL
----------------

Rich may be installed in the REPL so that Python data structures are automatically pretty printed with syntax highlighting. Here's how::

    >>> from rich import pretty
    >>> pretty.install() 
    >>> ["Rich and pretty", True]

You can also use this feature to try out Rich *renderables*. Here's an example::

    >>> from rich.panel import Panel
    >>> Panel.fit("[bold yellow]Hi, I'm a Panel", border_style="red")

Read on to learn more about Rich renderables.

IPython Extension
~~~~~~~~~~~~~~~~~

Rich also includes an IPython extension that will do this same pretty install + pretty tracebacks. Here's how to load it::

    In [1]: %load_ext rich
    
You can also have it load by default by adding `"rich"` to the ``c.InteractiveShellApp.extension`` variable in 
`IPython Configuration <https://ipython.readthedocs.io/en/stable/config/intro.html>`_.

Rich Inspect
------------

Rich has an :meth:`~rich.inspect` function which can generate a report on any Python object. It is a fantastic debug aid, and a good example of the output that Rich can generate. Here is a simple example::

    >>> from rich import inspect
    >>> from rich.color import Color
    >>> color = Color.parse("red")
    >>> inspect(color, methods=True)
