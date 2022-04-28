.. _full_screen_applications:

Text User Interface (Full screen applications)
================================================

`quo` can be used to create complex full screen terminal
applications. Typically, an application consists of a layout (to describe the
graphical part) and a set of key bindings.

The sections below describe the components required for full screen
applications (or custom, non full screen applications), and how to assemble
them together.

.. note::

    Also remember that the ``examples`` directory of the quo
    repository contains plenty of examples. Each example is supposed to explain
    one idea. So, this as well should help you get started.

    Don't hesitate to open a GitHub issue if you feel that a certain example is
    missing.


``A simple application``
------------------------

Almost every quo application is an instance of an :func:`~quo.container`. The simplest full screen example would look like this:

.. code:: python

 from quo import container
 from quo.widget import Label

 content = Label("Hello, world")

 container(content)

This will only consume the least amount of space required.

.. note::

        If we set the ``full_screen`` option, the application will run in an alternate screen buffer, in full screen mode.
       Starting with v2022.4.5, :kbd:`ctrl-c` will be the default key binder for to exit the app, you will still be able to define your own set of key bindings.

.. code:: python

 from quo import container
 from quo.widget import TextField

 content = TextField("Hello, world")
 container(content, bind=True, full_screen=True)
 
An application consists of several components. The most important are:

- I/O objects: the input and output device.
- The layout: this defines the graphical structure of the application. For
  instance, a text box on the left side, and a button on the right side.
- A style: this defines what colors and underline/bold/italic styles are used
  everywhere.
- A set of key bindings.

We will discuss all of these in more detail below.


``The layout``
----------------
Under the hood, class :class:`~quo.layout.Layout` is the layout for function :func:`~quo.container`.

.. code:: python

 """simple example of a a text area displaying `Hello World!` """
 
 from quo import container
 from quo.widget import Box, Frame, TextField
 
 # Layout for displaying hello world.
 # (The frame creates the border, the box takes care of the margin/padding.)
 
 content = Box(
            Frame(
              TextField("Hello, world!!")
               )
               )
               
 container(content, bind=True, full_screen=True)

In the example above, the Layout consists of :class:`Box`, :class:`Frame` and :class:`TextField` for displaying hello world.

The class :class:`Box` takes care of the margin/padding, class :class:`Frame` creates the border,  and class :class:`TextField` takes care of the text to be printed.
The :func:`quo.container` prints the layout to the output.


container
^^^^^^^^^^
Print the layout to the output

**Parameters**
     - ``container`` - AnyContaine
     - ``bind`` *(bool)* - When True, initiate a :class:`~quo.keys.Bind` instance for the key bindings.
     - ``full_screen`` *(bool)* - When True, run the application on the alternate screen buffer.
     - ``focused_element`` - element to be focused initially. *(Can be anything the `focus` function accepts.)*
     - ``mouse_support`` - :class:`~quo.filters.Filter` or boolean. When True, enable mouse support. 
     - ``style`` - A style string.

A layered layout architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways to create a layout, depending on how
customizable you want things to be. In fact, there are several layers of abstraction.

- The most low-level way of creating a layout is by combining
  :class:`~quo.layout.Container` and
  :class:`~quo.layout.UIControl` objects.

  Examples of :class:`~quo.layout.Container` objects are
  :class:`~quo.layout.VSplit` (vertical split),
  :class:`~quo.layout.HSplit` (horizontal split) and
  :class:`~quo.layout.FloatContainer`. These containers arrange the
  layout and can split it in multiple regions. Each container can recursively
  contain multiple other containers. They can be combined in any way to define
  the "shape" of the layout.

  The :class:`~quo.layout.Window` object is a special kind of
  container that can contain a :class:`~quo.layout.UIControl`
  object. The :class:`~quo.layout.UIControl` object is responsible
  for the generation of the actual content. The
  :class:`~quo.layout.Window` object acts as an adaptor between the
  :class:`~quo.layout.UIControl` and other containers, but it's also
  responsible for the scrolling and line wrapping of the content.

  Examples of :class:`~quo.layout.UIControl` objects are
  :class:`~quo.layout.BufferControl` for showing the content of an
  editable/scrollable buffer, and
  :class:`~quo.layout.FormattedTextControl` for displaying
  (:ref:`formatted <formatted_text>`) text.

  Normally, it is never needed to create new
  :class:`~quo.layout.UIControl` or
  :class:`~quo.layout.Container` classes, but instead you would
  create the layout by composing instances of the existing built-ins.

- A higher level abstraction of building a layout is by using "widgets". A
  widget is a reusable layout component that can contain multiple containers and controls.
  
Quo contains several widgets like:
  :class:`~quo.widget.Button`,
  :class:`~quo.widget.Frame`,
  :class:`~quo.widget.Label`,
  :class:`~quo.widget.TextField`,
  :class:`~quo.widget.VerticalLine` and so on.

- The highest level abstractions can be found in the ``dialog`` module.
  There we don't have to think about the layout, controls and containers at
  all. This is the simplest way to use quo, but is only meant for specific use cases, like a prompt or a simple dialog window.

Containers and controls
^^^^^^^^^^^^^^^^^^^^^^^

The biggest difference between containers and controls is that containers
arrange the layout by splitting the screen in many regions, while controls are
responsible for generating the actual content.

.. note::

   Under the hood, the difference is:

   - containers use *absolute coordinates*, and paint on a
     :class:`~quo.layout.screen.Screen` instance.
   - user controls create a :class:`~quo.layout.UIContent`
     instance. This is a collection of lines that represent the actual
     content. A :class:`~quo.layout.UIControl` is not aware
     of the screen.

+------------------------------------+-------------------------------------------+
| Abstract base class                | Examples                                  |
+====================================+===========================================+
| :class:`~quo.layout.Container`     | :class:`~quo.layout.HSplit`               |
|                                    | :class:`~quo.layout.VSplit`               |
|                                    | :class:`~quo.layout.FloatContainer`       |
|                                    | :class:`~quo.layout.Window`               |
|                                    | :class:`~quo.layout.ScrollablePane`       |
+------------------------------------+-------------------------------------------+
| :class:`~quo.layout.UIControl`     | :class:`~quo.layout.BufferControl`        |
|                                    | :class:`~quo.layout.FormattedTextControl` |
+------------------------------------+-------------------------------------------+

The :class:`~quo.layout.Window` class itself is
particular: it is a :class:`~quo.layout.Container` that
can contain a :class:`~quo.layout.UIControl`. Thus, it's the adaptor
between the two. The :class:`~quo.layout.Window` class also takes
care of scrolling the content and wrapping the lines if needed.

Finally, there is the :class:`~quo.layout.Layout` class which wraps
the whole layout. This is responsible for keeping track of which window has the
focus.

Here is an example of a layout that displays the content of the default buffer
on the left, and displays ``"Hello world"`` on the right. In between it shows a
vertical line:

.. code:: python

 from quo import container
 from quo.buffer import Buffer
 from quo.layout import BufferControl, FormattedTextControl, VSplit, Window

 buffer1 = Buffer()  # Editable buffer.

 content = VSplit([
        # One window that holds the BufferControl with the default buffer on the left.
      Window(BufferControl(buffer=buffer1)),

        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
      Window(width=1, char='|'),

        # Display the text 'Hello world' on the right.
      Window(FormattedTextControl('Hello world')),
  ])


 container(content, full_screen=True)

More complex layouts can be achieved by nesting multiple
:class:`~quo.layout.VSplit`,
:class:`~quo.layout.HSplit` and
:class:`~quo.layout.FloatContainer` objects.

If you want to make some part of the layout only visible when a certain
condition is satisfied, use a
:class:`~quo.layout.ConditionalContainer`.

Finally, there is :class:`~quo.layout.ScrollablePane`, a container
class that can be used to create long forms or nested layouts that are
scrollable as a whole.


``Key bindings``
-----------------

In order to react to user actions, we need to create a
:class:`~quo.keys.Bind` object using :meth:`quo.keys.bind`

There are two kinds of key bindings:

- Global key bindings, which are always active.
- Key bindings that belong to a certain
  :class:`~quo.layout.controls.UIControl` and are only active when
  this control is focused. Both
  :class:`~quo.layout.BufferControl`
  :class:`~quo.layout.FormattedTextControl` takes a ``bind``
  argument.


Global key bindings
^^^^^^^^^^^^^^^^^^^

Key bindings can be passed to the application as follows:

.. code:: python

 from quo import container
 from quo.keys import bind

 container(bind=True)

Registering Key bindings
^^^^^^^^^^^^^^^^^^^^^^^^^^
To register a new keyboard shortcut, we can use the
:meth:`~quo.keys.Bind.add` method as a decorator of the key handler:

.. code:: python   

 from quo import container
 from quo.keys import bind
 from quo.widget import TextField
 
 content = TextField("Hello, world")
 
 # A custom Key binder to exit the application
 @bind.add("ctrl-q")
 def exit_(event):
       """
       Pressing "ctrl-q" will exit the user interface
       """
        event.app.exit()
        
 container(content, bind=True, full_screen=True)


The callback function is named ``exit_`` for clarity, but it could have been named ``_`` (underscore) as well, or anything you see fit

Read more about `key bindings <https://quo.readthedocs.io/en/latest/kb.html>`_


HSplit
--------
Several layouts, one stacked above/under the other. like so::

        +--------------------+
        |                    |
        +--------------------+
        |                    |
        +--------------------+
        
By default, this doesn't display a horizontal line between the children, but if this is something you need, then create a HSplit as follows:

.. code:: python

 HSplit(subset=[ ... ], padding_char='-', padding=1, padding_style='fg:red')

**Parameters**

  - ``subset`` - List of child :class:`.Container` objects.
  - ``window_too_small`` - A :class:`.Container` object that is displayed if there is not enough space for all the subsets. By default, this is a "Window too small" message.
  - ``align`` - A `VerticalAlign` value. i.e ``top``, ``center``, ``bottom`` or ``justify``
  - ``width`` - When given, use this width instead of looking at the subsets.
  - ``height`` -  When given, use this height instead of looking at the subsets.
  - ``z_index``-  (int or None) When specified, this can be used to bring element in front of floating elements.  `None` means: inherit from parent.
  - ``style`` - A style string.
  - ``modal`` *(bool)* - Setting ``modal=True`` makes what is called a **modal** container. Normally, a subset container would inherit its parent key bindings. This does not apply to **modal** containers.
  
  - ``bind`` - ``None`` or a :class:`.Bind` object.
  - ``padding`` - (`Dimension` or int), size to be used for the padding.                  - ``padding_char`` - Character to be used for filling in the padding.
  - ``padding_style`` - Style to applied to the padding.
    
.. code:: python

 from quo import container
 from quo.layout import HSplit, Window
 from quo.widget import Label
 
 # 1. The layout
 content = HSplit([
        Label("\n\n(Top pane)"),
        Window(height=1, char="-"),  # Horizontal line in the middle.
        Label("\n\n(Bottom pane)")
        ])
        
  # 2. The `Application`
  # Press `ctrl-c` to exit 
 container(content, bind=True)



VSplit
--------

Several layouts, one stacked left/right of the other like so::

        +---------+----------+
        |         |          |
        |         |          |
        +---------+----------+


By default, this doesn't display a vertical line between the children, but if this is something you need, then create a VSplit as follows:

.. code:: python

 VSplipt([ ... ], padding_char='|', padding=1, padding_style='fg:blue')

**Parameters**
    - ``subset`` - List of subsets :class:`.Container` objects.
    - ``window_too_small`` - A :class:`.Container` object that is displayed if there is not enough space for all the children. By default, this is a "Window too small" message.
    - ``align``- A `HorizontalAlign` value. i.e ``left``, ``centre``, ``right`` or ``justify``
    - ``width`` - When given, use this width instead of looking at the subsets.
    - ``height`` - When given, use this height instead of looking at the subsets.
    - ``z_index`` - (int or None) When specified, this can be used to bring element in front of floating elements.  `None` means: inherit from parent.
    - ``style`` - A style string.
    - ``modal`` *(bool)* - Setting ``modal=True`` makes what is called a **modal** container. Normally, a subset container would inherit its parent key bindings. This does not apply to **modal** containers.
    - ``bind`` - ``None`` or a :class:`.Bind` object.
    - ``padding`` - (`Dimension` or int), size to be used for the padding.
    - ``padding_char`` - Character to be used for filling in the padding.
    - ``padding_style`` - Style to applied to the padding.

.. code:: python

 # Press `ctrl-c` to exit
 from quo import container
 from quo.layout import VSplit, Window
 from quo.widget import Label
 
 # 1. The layout
 content = VSplit([
          Label("(Left pane)"),
          Window(width=1, char="|"), # Vertical line in the middle.
          Label("(Right pane)")
          ])
          
 container(content, bind=True, full_screen=True)
 

 
:class:`~quo.layout.VSplit` and :class:`~quo.layout.HSplit` take a ``modal`` argument.

Setting ``modal=True`` makes what is called a **modal** container. Normally, a child container would inherit its parent key bindings. This does not apply to **modal** containers.

Consider a **modal** container (e.g. :class:`~quo.layout.VSplit`)
is child of another container, its parent. Any key bindings from the parent are not taken into account if the **modal** container (subset) has the focus.

This is useful in a complex layout, where many controls have their own key bindings, but you only want to enable the key bindings for a certain region of the layout.

The global key bindings are always active.

Window
^^^^^^^^
:class:`~quo.layout.Window` is a :class:`~quo.layout.Container` that wraps a :class:`~quo.layout.UIControl`, like a :class:`~quo.layout.BufferControl` or :class:`~quo.layout.FormattedTextControl`.

**Parameters**
    - ``content`` - :class:`.UIControl` instance.
    - ``width`` - :class:`.Dimension` instance or callable.
    - ``height`` - :class:`.Dimension` instance or callable.
    - ``z_index`` - When specified, this can be used to bring element in front of floating elements.
    - ``dont_extend_width`` *(bool)* - When `True`, don't take up more width then the preferred width reported by the control.
    - ``dont_extend_height`` *(bool)* - When `True`, don't take up more width then the  preferred height reported by the control.
    - ``ignore_content_width`` *(bool)* - A `bool` or :class:`.Filter` instance. Ignore the :class:`.UIContent` width when calculating the dimensions.
    - ``ignore_content_height`` *(bool)* - A `bool` or :class:`.Filter` instance. Ignore the :class:`.UIContent` height when calculating the dimensions.
    - ``left_margins`` - A list of :class:`.Margin` instance to be displayed on the left. For instance: :class:`~quo.layout.NumberedMargin` can be one of them in order to show line numbers.
    - ``right_margins`` - Like `left_margins`, but on the other side.
    - ``scroll_offsets`` - :class:`.ScrollOffsets` instance, representing the preferred amount of lines/columns to be always visible before/after the cursor. When both top and bottom are a very high number, the cursor will be centered vertically most of the time.
    - ``allow_scroll_beyond_bottom`` *(bool)* - A `bool` or :class:`.Filter` instance. When True, allow scrolling so far, that the top part of the content is not visible anymore, while there is still empty space available at the bottom of the window. In the Vi editor for instance, this is possible. You will see tildes while the top part of the body is hidden.
    - ``wrap_lines`` *(bool)** - A `bool` or :class:`.Filter` instance. When True, don't scroll horizontally, but wrap lines instead.
    - ``get_vertical_scroll`` - Callable that takes this window instance as input and returns a preferred vertical scroll. *(When this is `None`, the scroll is only determined by the last and current cursor position.)*
    - ``get_horizontal_scroll`` - Callable that takes this window instance as input and returns a preferred vertical scroll.
    - ``always_hide_cursor`` *(bool)* - A `bool` or :class:`.Filter` instance. When True, never display the cursor, even when the user control specifies a cursor position.
    - ``cursorline`` *(bool)* - A `bool` or :class:`.Filter` instance. When True, display a cursorline.
    - ``cursorcolumn`` *(bool)* - A `bool` or :class:`.Filter` instance When True, display a cursorcolumn.
    - ``colorcolumns`` - A list of :class:`.ColorColumn` instances that describe the columns to be highlighted, or a callable that returns such a list.
    - ``align`` - :class:`.WindowAlign` value or callable that returns an :class:`.WindowAlign` value. alignment of content. i.e ``left``, ``centre`` or ``right``
    - ``style`` - A style string. Style to be applied to all the cells in this  window. *(This can be a callable that returns a string.)*
    - ``char`` *(str)* - Character to be used for filling the background. This can also be a callable that returns a character.
    - ``get_line_prefix`` - None or a callable that returns formatted text to  atted text to be inserted before a line. It takes a line number (int) and a wrap_count and returns formatted text. This can be used for implementation of line continuations, things like Vim "breakindent".
      
FloatContainer
^^^^^^^^^^^^^^^
Container which can contain another container for the background, as well as a list of floating containers on top of it.

**Parameters**

     - ``content`` - :class:`.AnyContainer` object
     - ``z_index`` - (int or None) When specified, this can be used to bring element in front of floating elements.  `None` means: inherit from parent.  This is the z_index for the whole `Float` container as a whole.
     - ``floats`` - List of :class:`.Float` object.
     - ``modal`` *(bool)* - Setting ``modal=True`` makes what is called a **modal** container. Normally, a subset container would inherit its parent key bindings. This does not apply to **modal** containers.
     - ``bind`` - ``None`` or a :class:`.Bind` object.
     - ``style`` - A style string.

Example Usage:

.. code:: python

 FloatContainer(
                Window(...),
                floats=[
                      Float(
                         xcursor=True,
                         ycursor=True,
                         content=CompletionsMenu(...)
                           )
                           ]
                          
                          
ConditionalContainer
^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to make some part of the layout only visible when a certain condition is satisfied, use a ConditionalContainer.
The received `filter` determines whether the given container should be displayed or not.

**Parameters**

     - ``content`` - :class:`.Container` instance.
     - ``filter`` - :class:`.Filter` instance.

    
 ``More about buffers and BufferControl``
------------------------------------------


Input processors
^^^^^^^^^^^^^^^^

A :class:`~quo.layout.processors.Processor` is used to postprocess
the content of a :class:`~quo.layout.BufferControl` before it's
displayed. It can for instance highlight matching brackets or change the
visualisation of tabs and so on.

A :class:`~quo.layout.processors.Processor` operates on individual
lines. Basically, it takes a (formatted) line and produces a new (formatted)
line.

Some build-in processors:

+-----------------------------------------------------------------+----------------------------------------------------------------------+
| Processor                                                       |                      Usage:                                          |
+=================================================================+======================================================================+
| :class:`~quo.layout.processors.HighlightSearchProcessor`        |           Highlight the current search results.                      |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.HighlightSelectionProcessor`     |           Highlight the selection.                                   |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.PasswordProcessor`               |           Display input as asterisks. (``*`` characters).            |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.BracketsMismatchProcessor`       |           Highlight open/close mismatches for brackets.              |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.BeforeInput`                     |           Insert some text before.                                   |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.AfterInput`                      |           Insert some text after.                                    |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.AppendAutoSuggestion`            |           Append auto suggestion text.                               |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.ShowLeadingWhiteSpaceProcessor`  |           Visualise leading whitespace.                              |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.ShowTrailingWhiteSpaceProcessor` |           Visualise trailing whitespace.                             |
+-----------------------------------------------------------------+----------------------------------------------------------------------+
| :class:`~quo.layout.processors.TabsProcessor`                   |           Visualise tabs as `n` spaces, or some symbols.             |
+-----------------------------------------------------------------+----------------------------------------------------------------------+

A :class:`~quo.layout.BufferControl` takes only one processor as
input, but it is possible to "merge" multiple processors into one with the :func:`~quo.layout.processors.merge_processors` function


» Check out more examples `here <https://github.com/scalabli/quo
/tree/master/examples/full-screen/>`_

