Widgets
========

A collection of reusable components for building full screen applications.

Box
----
Add padding around a container.
This also makes sure that the parent can provide more space than required by the child. This is very useful when wrapping a small element  with a fixed size into a ``VSplit`` or ``HSplit`` object.
The ``HSplit`` and ``VSplit`` try to make sure to adapt respectively the width and height, possibly
shrinking other elements. Wrapping something in a ``Box`` makes it flexible.

**Parameters**
     - ``body`` - Another container object.
     - ``padding`` - The margin to be used around the body. This can be overriddenby :param:`padding_left`, :param:`padding_right`, :param:`padding_top` and :param:`padding_bottom` parameters.
     - ``style`` - A style string.
     - ``char``  - Character to be used for filling the space around the body. *(This is supposed tobe a character with a terminal width of 1.)*

.. code:: python

  from quo import Console
  from quo.widgets import Box, Labe
  from quo.keys import KeyBinder
  from quo.layout import Layout, HSplit
  from quo.style import Style

  # Styling for the label
  example_style = Style(                                                  [
            ("hello-world", "bg:red fg:black")
            ]
        )

  root = Box(
          HSplit(                                                             [
          Label("Hello, World", style="class:hello-world")
                ]
                ), padding=2, char="|")

  layout = Layout(container=root)

  kb = KeyBinder()

  @kb.add("ctrl-c")                                               def _(event):
     event.app.exit()
    
  Console(
     layout=layout,
     bind=kb,
     style=example_style,
     full_screen=True).run()

