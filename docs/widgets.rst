Widgets
========

A collection of reusable components for building full screen applications.


``Label``
---------
Widget that displays the given text. It is not editable or focusable.

**Parameters**
    - ``text`` - Text to display. Can be multiline. All value types accepted by :class:`quo.layout.FormattedTextControl` are allowed, including a callable.
    - ``style`` - A style string.
    - ``width`` - When given, use this width, rather than calculating it from the text size.
    - ``dont_extend_width`` - When `True`, don't take up more width than preferred, i.e. the length of the longest line of the text, or value of `width` parameter, if given. `True` by default
    - ``dont_extend_height`` -  When `True`, don't take up more width than the preferred height, i.e. the number of lines of the text. `False` by default.

.. code:: python

   from quo import Console
   from quo.widgets import Label
   from quo.keys import KeyBinder
   from quo.layout import Layout
   from quo.style import Style

   # Styling for the label
   example_style = Style(
          [
          ("hello-world", "bg:red fg:black")
          ]
      )

   root = Label("Hello, World", style="class:hello-world")

   layout = Layout(container=root)

   kb = KeyBinder()

   @kb.add("ctrl-c")
   def _(event):
      event.app.exit()

   Console
   layout=layout,
   bind=kb,
   style=example_style,
   full_screen=True).run()


``Box``
-------
Add padding around a container.
This also makes sure that the parent can provide more space than required by the child. This is very useful when wrapping a small element  with a fixed size into a ``VSplit`` or ``HSplit`` object.
The ``HSplit`` and ``VSplit`` try to make sure to adapt respectively the width and height, possibly
shrinking other elements. Wrapping something in a ``Box`` makes it flexible.

**Parameters**
     - ``body`` - Another container object.
     - ``padding`` - The margin to be used around the body. This can be overriddenby :param:`padding_left`, :param:`padding_right`, :param:`padding_top` and :param:`padding_bottom` parameters.
     - ``style`` - A style string.
     - ``char``  - Character to be used for filling the space around the body. *(This is supposed to be a character with a terminal width of 1.)*

.. code:: python

  from quo import Console
  from quo.widgets import Box, Label
  from quo.keys import KeyBinder
  from quo.layout import Layout
  from quo.style import Style

  # Styling for the label
  example_style = Style(
     [
     ("hello-world", "bg:red fg:black") 
     ]
     )
     
  root = Box(
          Label("Hello, World", style="class:hello-world"), padding=5)
          
          
  layout = Layout(container=root)
  
  kb = KeyBinder()

  @kb.add("ctrl-c")
  def _(event):
      event.app.exit()
    
  Console(
     layout=layout,
     bind=kb,
     style=example_style,
     full_screen=True).run()

