.. _printing_text:

Printing (and using) formatted text
===================================

``echo``
--------
:func:`quo.echo` prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode, binary data and formatted text. It will emit  newline by default, which cab be suppressed by passing :param: ``nl=False``

**Parameters**
      * ``text`` – the string to style with ansi or rgb color codes.
      * ``fg``  – if provided this will become the foreground color.
      * ``bg``  – if provided this will become the background color.
      * ``bold``  – if provided this will enable or disable bold mode.
      * ``dim``  – if provided this will enable or disable dim mode.
      * ``nl`` - if provided this will print a new line.
      * ``ul or underline`` – if provided this will enable or disable underline.
      * ``italic`` - if provided this will print data in italic.
      * ``blink`` – if provided this will enable or disable blinking.
      * ``strike`` -if provided this will print a strikethrough text.
      * ``hidden`` - if privided this will prevent the input from getting printed.
      * ``reverse`` – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).
      * ``reset``  – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

.. code:: python

 from quo import echo

 echo("Hello, world!", nl=False)

.. code:: python

 from quo import echo

 echo(b'\xe2\x98\x83')

Printing to Standard error
^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can easily print to standard error by passing :param:``err=True``

.. code:: python

 from quo import echo
 
 echo('Hello World!', err=True)
 
Here's a list of supported color names:

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

``print``
----------
quo ships with a :func:`~quo.print` function that's meant to be (as much as possible) compatible with the built-in print function, and :func:`quo.echo`. It also supports color and formatting just like :func:`quo.echo` 
On Linux systems, this will output VT100 escape sequences, while on Windows it will use Win32 API calls or VT100 sequences, depending on what is available.

.. note::

        This page is also useful if you'd like to learn how to use formatting
        in other places, like in a prompt or a toolbar.

``Formatted text``
-------------------

There are several ways to display colors:

- By creating a :func:`quo.echo` object.
- By creating an :class:`~quo.text.Text` object
- By creating a list of ``(style, text)`` tuples.


An instance of any of these three kinds of objects is called "formated text".

Using quo.echo
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from quo import echo

   echo("This is bold", bold=True)
   echo("This is italic", italic=True)
   echo("This is underlined", underline=True)

   # Colors from the ANSI palette

   echo("This is red", fg="red")
   echo("This is green", fg="green")




Using quo.text.Text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`~quo.text.Text` can be used to indicate that a string contains HTML-like formatting. It recognizes the basic tags for bold, italic and underline: ``<b>``, ``<i>`` and ``<u>``.

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




Using (style, text) tuples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is possible to create styles and text tuples using :class:`~quo.text.FormattedText` class
.. code:: python
   
  from quo import print
  from quo.text import FormattedText

  text = FormattedText([
      ('fg:red', 'Hello'),
      ('', ' '),
      ('fg:blue italic', 'World'),
  ])

  print(text)
Similar to the :class:`~quo.text.Text` example, it is also possible to use class names, and separate the styling in a style sheet.

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


» Check out more examples `here <https://github.com/scalabli/quo/tree/master/examples/print-text/>`
