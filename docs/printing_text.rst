.. _printing_text:

Printing (and using) formatted text
===================================

``echo``
--------
:func:`quo.echo` prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode, binary data and formatted text.

Supported color names:

* ``black (might be a gray)``
* ``red``
* ``green``
* ``yellow`` *(might be an orange)*
* ``blue``
* ``magenta``
* ``cyan``
* ``white`` *(might be light gray)*
* ``vblack``  *vibrant black*
* ``vblue``
* ``vmagenta``
* ``vwhite``
* ``vcyan``
* ``vred``
* ``vgreen``
* ``vyellow``

RGB color codes


Parameters
   * ``text`` – the string to style with ansi codes.

   * ``fg``  – if provided this will become the foreground color.

   * ``bg``  – if provided this will become the background color.

   * ``bold``  – if provided this will enable or disable bold mode.

   * ``dim``  – if provided this will enable or disable dim mode.

   * ``nl`` - if provided this will print a new line.

   * ``ul or underline`` – if provided this will enable or disable underline

   * ``italic`` - if provided this will print data in italics

   * ``blink`` – if provided this will enable or disable blinking.

   * ``strike`` -if provided this will print a strikethrough text

   * ``hidden`` - if privided this will prevent the input from getting printed

   * ``reverse`` – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).

   * ``reset``  – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

``print``
----------
quo ships with a
:func:`~quo.print` function that's meant to
be (as much as possible) compatible with the built-in print function, and :func:`quo.echo`. It also supports colors and formatting jist link :func:`quo.echo` 
On Linux systems, this will output VT100 escape sequences, while on Windows it
will use Win32 API calls or VT100 sequences, depending on what is available.

.. note::

        This page is also useful if you'd like to learn how to use formatting
        in other places, like in a prompt or a toolbar. Just like
        :func:`~quo.print` takes any kind
        of "formatted text" as input, prompts and toolbars also accept "formatted text".


``Formatted text``
-------------------

There are several ways to display colors:

- By creating a :func:`quo.echo` object.
- By creating an :class:`~quo.text.Text` object
- By creating a list of ``(style, text)`` tuples.


An instance of any of these three kinds of objects is called "formated text".

``[1] Using quo.echo``
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from quo import echo

   echo("This is bold", bold=True)
   echo("This is italic", italic=True)
   echo("This is underlined", underline=True)

   # Colors from the ANSI palette

   echo("This is red", fg="red")
   echo("This is green", fg="green")




``[2] Using quo.text.Text``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`~quo.text.Text` can be used to indicate that a
string contains HTML-like formatting. It recognizes the basic tags for bold,
italic and underline: ``<b>``, ``<i>`` and ``<u>``.

.. code:: python

    from quo import print
    from quo.text import Text

    print(Text('<b>This is bold</b>'))
    print(Text('<i>This is italic</i>'))
    print(Text('<u>This is underlined</u>'))

.. code:: python

    # Colors from the ANSI palette.
    print(Text('<red>This is red</red>'))
    print(Text('<green>This is green</green>'))

    # Named colors (256 color palette, or true color, depending on the output).
    print(Text('<skyblue>This is sky blue</skyblue>'))
    print(Text('<seagreen>This is sea green</seagreen>'))
    print(Text('<violet>This is violet</violet>'))

Both foreground and background colors can also be specified setting the `fg`
and `bg` attributes of any HTML tag:

.. code:: python

    # Colors from the ANSI palette.
    print(Text('<aaa fg="white" bg="green">White on green</aaa>'))

Underneath, all Text tags are mapped to classes from a stylesheet, so you can
assign a style for a custom tag.

.. code:: python

    from quo.style import Style
    from quo.text import Text

    style = Style.add({
        'aaa': 'fg:red',
        'bbb': 'fg:blue italic',
    })

    print(Text('<aaa>Hello</aaa> <bbb>world</bbb>!'), style=style)




``(style, text) tuples``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Internally, :class:`~quo.text.Text` objects are mapped to a list of
``(style, text)`` tuples. It is however also possible to create such a list
manually with :class:`~quo.text.FormattedText` class.
This is a little more verbose, but it's probably the most powerful way of expressing formatted text.

.. code:: python
   
    from quo import print
    from quo.text import FormattedText

    text = FormattedText([
        ('fg:red', 'Hello'),
        ('', ' '),
        ('fg:blue italic', 'World'),
    ])

    print(text)

Similar to the :class:`~quo.text.Text` example, it is also
possible to use class names, and separate the styling in a style sheet.

.. code:: python

    from quo import print
    from quo.text import FormattedText
    from quo.style import Style
    # The text.
    text = FormattedText([
        ('class:aaa', 'Hello'),
        ('', ' '),
        ('class:bbb', 'World'),
    ])

    # The style sheet.
    style = Style.add({
        'aaa': 'fg:red',
        'bbb': 'fg:green italic',
    })

    print(text, style=style)


``Pygments ``(Token, text)`` tuples``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you have a list of `Pygments <http://pygments.org/>`_ ``(Token, text)``
tuples, then these can be printed by wrapping them in a
:class:`~quo.text.PygmentsTokens` object.

.. code:: python
     
    from quo import print
    from quo.text import PygmentsToken
    from pygments.token import Token
    
    text = [
        (Token.Keyword, 'print'),
        (Token.Punctuation, '('),
        (Token.Literal.String.Double, '"'),
        (Token.Literal.String.Double, 'hello'),
        (Token.Literal.String.Double, '"'),
        (Token.Punctuation, ')'),
        (Token.Text, '\n'),
    ]

    print(PygmentsTokens(text))


Similarly, it is also possible to print the output of a Pygments lexer:

.. code:: python

    import pygments
    from pygments.token import Token
    from pygments.lexers.python import PythonLexer
    from quo import print
    from quo.text import PygmentsTokens


    # Printing the output of a pygments lexer.
    tokens = list(pygments.lex('print("Hello")', lexer=PythonLexer()))
    print(PygmentsTokens(tokens))

Quo ships with a default colorscheme which styles it just like
Pygments would do, but if you'd like to change the colors, keep in mind that
Pygments tokens map to classnames like this:

+-----------------------------------+---------------------------------------------+
| pygments.Token                    | quo classname                               |
+===================================+=============================================+
| - ``Token.Keyword``               | - ``"class:pygments.keyword"``              |
| - ``Token.Punctuation``           | - ``"class:pygments.punctuation"``          |
| - ``Token.Literal.String.Double`` | - ``"class:pygments.literal.string.double"``|
| - ``Token.Text``                  | - ``"class:pygments.text"``                 |
| - ``Token``                       | - ``"class:pygments"``                      |
+-----------------------------------+---------------------------------------------+

A classname like ``pygments.literal.string.double`` is actually decomposed in
the following four classnames: ``pygments``, ``pygments.literal``,
``pygments.literal.string`` and ``pygments.literal.string.double``. The final
style is computed by combining the style for these four classnames. So,
changing the style from these Pygments tokens can be done as follows:

.. code:: python

    from quo import print
    from quo.style import Style

    style = Style.add({
        'pygments.keyword': 'underline',
        'pygments.literal.string': 'bg:#00ff00 #ffffff',
    })
    print(PygmentsTokens(tokens), style=style)

