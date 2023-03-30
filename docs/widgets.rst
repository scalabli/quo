Widgets
========

A collection of reusable components for building full screen applications.

When in ``full_screen`` mode, the default key binder to exit the application is ``Ctrl-C``, however you can set your own.


``Frame``
---------

Draw a border around any container, optionally with a title text.
Changing the title and body of the frame is possible at runtime by assigning to the `body` and `title` attributes of this class.

**Parameters**
      - ``body`` - Another container object.
      - ``title`` - Text to be displayed in the top of the frame *(can be formatted text)*
      - ``style`` - Style string to be applied to this widget.
      - ``width`` - Frame width
      - ``height`` - Frame height.

.. code:: python

  from quo import container
  from quo.widget import Frame, Label


  root = Frame(
            Label("Hello, World!"),
            title="Quo: python")
       
  @bind.add("ctrl-c")
  def _(event):
         event.app.exit()
  
  container(root, bind=True, full_screen=True)                           


.. image:: ./images/widgets/label.png



``Box``
-------
Add padding around a container.
This also makes sure that the parent can provide more space than required by the child. This is very useful when wrapping a small element  with a fixed size into a ``VSplit`` or ``HSplit`` object.

**Parameters**
     - ``body`` - Another container object.
     - ``padding`` - The margin to be used around the body. This can be overridden by :param:`padding_left`, :param:`padding_right`, :param:`padding_top` and :param:`padding_bottom` parameters.
     - ``fg`` *(Optional[str])* - A foregound color string.
     - ``bg`` *(Optional[str])* - A background color string.
     - ``char``  *(Optional[str])* - Character to be used for filling the space around the body. *(This is supposed to be a character with a terminal width of 1.)*

.. code:: python

   from quo import container
   from quo.box import Box
   from quo.keys import bind
   from quo.label import Label

   label = Label("<fg='black' bg='red'>Hello, World</style>")

   content = Box(label, padding=5)

   # Press `q` to cancel
   @bind.add("q")
   def _(event):
     event.app.exit()

   container(content, bind=True, full_screen=True)  
     
``Label``
---------
Widget that displays the given text. It is not editable or focusable.

**Parameters**
    - ``text`` - Text to display. Can be multiline.
    - ``width`` - When given, use this width, rather than calculating it from the text size.
    - ``flexible_width`` *(bool)* - When `False`, don't take up more width than preferred, i.e. the length of the longest line of the text, or value of `width` parameter, if given. `True` by default
    - ``flexible_height`` *(bool)*-  When `False`, don't take up more width than the preferred height, i.e. the number of lines of the text. `True` by default.

*(Changed on v2023.3)*
   
You can print the layout to the output in a non-interactive way like so:

.. code:: python

   from quo import container
   from quo.label import Label

   content = Label("<fg='black' bg='red'>Hello, World</style>")
   container(content)

.. image:: ./images/widgets/label.png
 

To make it fullscreen set :param:`bind` and :param:`full_screen` to ``True`` Press :kbd:`Ctrl-C` to quit 

.. code:: python

   from quo import container
   from quo.label import Label

   content = Label("<fg='black' bg='red'>Hello, World</style>")
   container(content, bind=True, full_screen=True)

.. image:: ./images/widgets/label-fullscreen.png

Adding a custom key binder
 
.. code:: python

   from quo import container
   from quo.keys import bind
   from quo.label import Label

   content = Label("<fg='black' bg='red'>Hello, World</style>")

   #Press Ctrl-a to exit
   @bind.add("ctrl-a")
   def _(event):
      event.app.exit()

   container(content, bind=True, full_screen=True)





``TextField``
--------------
A simple input field.
This is a higher level abstraction on top of several other classes with sane defaults.

This widget does have the most common options, but it does not intend to cover every single use case.

**Parameters**
- ``text`` *(str)* - The initial text.
- ``prompt`` *(Optional[TextFieldFormattedText, str])* - Prompt. ie *<blue>What is your name?</blue>*
- ``multiline`` *(bool)* - If True, allow multiline input.
- ``completer`` - :class:`~quo.ompletion.Completer` instance for auto completion.
- ``complete_while_typing`` -  Boolean.
- ``accept_handler`` - Called when `Enter` is pressed *(This should be a callable that takes a buffer as input)*.
- ``history`` - :class:`~quo.history.History` instance.
- ``auto_suggest`` - :class:`~quo.completion.auto_suggest.AutoSuggest` instance for input suggestions.
- ``hide`` *(bool)* -  When `True`, display using asterisks.
- ``focusable`` *(bool)* -  When `True`, allow this widget to receive the focus.
- ``focus_on_click`` *(bool)* -  When `True`, focus after mouse click.
- ``input_processors`` - `None` or a list of :class:`~quo.layout.Processor` objects.
- ``type`` - `None` or a :class:`~quo.types.Validator` object.
- ``highlighter`` - :class:`~quo.highlight.Lexer` instance for syntax highlighting.
- ``wrap_lines`` *(bool)* - When `True`, don't scroll horizontally, but wrap lines.
- ``width`` - Window width. (:class:`~quo.layout.Dimension` object.)
- ``height`` - Window height. (:class:`~quo.layout.Dimension` object.)
- ``scrollbar`` *(bool)* - When `True`, display a scroll bar.
- ``fg`` *(Optional[str])* - A foregound color string.
- ``bg`` *(Optional[str])* - A background color string.
- ``flexible_width`` *(bool)* - When `False`, don't take up more width than the preferred width reported by the control.
- ``flexible_height`` *(bool)* - When `False`, don't take up more width than the preferred height reported by the control.
- ``get_line_prefix`` - None or a callable that returns formatted text to be inserted before a line. It takes a line number *(int)* and a wrap_count and returns formatted text. This can be used for implementation of line continuations, things like Vim "breakindent" and so on.

Other attributes
^^^^^^^^^^^^^^^^^
- ``search_field`` - An optional `SearchToolbar` object.



     
``Button``
------------

Clickable button.

**Parameters**
      - ``text`` - The caption for the button.
      - ``handler`` - `None` or callable. Called when the button is clicked. No parameters are passed to this callable. Use for instance Python's `functools.partial` to pass parameters to this callable if needed.
      - ``width`` - Width of the button. 

      

``Shadow``
-----------

Draw a shadow underneath/behind this container. *(This applies `class:shadow` the the cells under the shadow. The Style should define the colors for the shadow.)*

**Parameters**
      - ``body`` - Another container object.
