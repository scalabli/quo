.. _full_screen_applications:

Full screen applications
=================================

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

Almost every quo application is an instance of an :class:`~quo.Suite` object. The simplest full screen example would look like this:

.. code:: python

    import quo

    app = quo.Suite(full_screen=True)
    app.run()

This will display an application with no layout specified.

.. note::

        If we wouldn't set the ``full_screen`` option, the application would
        not run in the alternate screen buffer, and only consume the least
        amount of space required for the layout.

An application consists of several components. The most important are:

- I/O objects: the input and output device.
- The layout: this defines the graphical structure of the application. For
  instance, a text box on the left side, and a button on the right side.
- A style: this defines what colors and underline/bold/italic styles are used
  everywhere.
- A set of key bindings.

We will discuss all of these in more detail below.


``I/O objects``
---------------

Every :class:`~quo.Suite` instance requires an I/O
object for input and output:

    - An :class:`~quo.input.Input` instance, which is an abstraction
      of the input stream (stdin).
    - An :class:`~quo.output.Output` instance, which is an
      abstraction of the output stream, and is called by the renderer.

Both are optional and normally not needed to pass explicitly. Usually, the
default works fine.

There is a third I/O object which is also required by the application, but not
passed inside. This is the event loop, an
:class:`~quo.eventloop` instance. This is basically a
while-true loop that waits for user input, and when it receives something (like
a key press), it will send that to the the appropriate handler, like for
instance, a key binding.

When :func:`~quo.Suite.run()` is called, the event
loop will run until the application is done. An application will quit when 
:func:`~quo.Suite.exit()` is called.


``The layout``
-------------

``Margins``
^^^^^^^^^^^^
Margins are used for displaying line numbers and scroll bars, but could be used to display any other kind of information as well.

.. code:: python

 import quo
 from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
 from prompt_toolkit.layout.margins import NumberedMargin, ScrollbarMargin
 
 intro = """ Quo is scallable\n""" * 30
 
 # Create text buffers. The margins will update if you scroll up or down.
 
 buff = quo.buffer.Buffer()
 buff.text = LIPSUM

 # 1. The layout
 hsplit = quo.layout.HSplit
 window = quo.layout.Window

 window1 = window(FormattedTextControl('Press "q" to quit.'), height= 1, style="bg:red fg:yellow")

 window2 = window(BufferControl(buffer=buff),                                        # Add margins
            left_margins=[NumberedMargin(), ScrollbarMargin()],
            right_margins=[ScrollbarMargin(), ScrollbarMarg
in()])

 body = hsplit(
    [
    window1,
    window2
    ]
)
# 2 Key bindings
 kb = quo.keys.KeyBinder()

@kb.add("q")
@kb.add("ctrl-c")
def _(event):
    "Quit application."
    event.app.exit()

# Layout
layout = quo.layout.Layout
A layered layout architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways to create a layout, depending on how
customizable you want things to be. In fact, there are several layers of
abstraction.

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
  widget is a reusable layout component that can contain multiple containers
  and controls. Widgets have a ``__pt_container__`` function, which returns
  the root container for this widget. Quocontains several widgets like :class:`~quo.widgets.TextArea`,
  :class:`~quo.widgets.Button`,
  :class:`~quo.widgets.Frame`,
  :class:`~quo.widgets.VerticalLine` and so on.

- The highest level abstractions can be found in the ``shortcuts`` module.
  There we don't have to think about the layout, controls and containers at
  all. This is the simplest way to use quo, but is only meant for
  specific use cases, like a prompt or a simple dialog window.

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

    import quo

    buffer1 = quo.buffer.Buffer()  # Editable buffer.

    root_container = quo.layout.VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        quo.layout.Window(content=quo.layout.BufferControl(buffer=buffer1)),

        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        quo.layout.Window(width=1, char='|'),

        # Display the text 'Hello world' on the right.
        quo.layout.Window(content=quo.layout.FormattedTextControl(text='Hello world')),
    ])

    layout = quo.layout.Layout(root_container)

    app = quo.Suite(layout=layout, full_screen=True)
    app.run() # You won't be able to Exit this app

Notice that if you execute this right now, there is no way to quit this
application yet. This is something we explain in the next section below.

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


Focusing windows
^^^^^^^^^^^^^^^^^

Focusing something can be done by calling the
:meth:`~quo.layout.Layout.focus` method. This method is very
flexible and accepts a :class:`~quo.layout.Window`, a
:class:`~quo.buffer.Buffer`, a
:class:`~quo.layout.controls.UIControl` and more.

In the following example, we use :func:`~quo.suite.get_app`
for getting the active application.

.. code:: python

    import quo

    # This window was created earlier.
    w = Window()

    # ...

    # Now focus it.
    quo.suite.get_app().layout.focus(w)

Changing the focus is something which is typically done in a key binding, so
read on to see how to define key bindings.

``Key bindings``
-----------------

In order to react to user actions, we need to create a
:class:`~quo.keys.KeyBinder` object and pass
that to our :class:`~quo.Suite`.

There are two kinds of key bindings:

- Global key bindings, which are always active.
- Key bindings that belong to a certain
  :class:`~quo.layout.controls.UIControl` and are only active when
  this control is focused. Both
  :class:`~quo.layout.BufferControl`
  :class:`~quo.layout.FormattedTextControl` take a ``bind``
  argument.


Global key bindings
^^^^^^^^^^^^^^^^^^^

Key bindings can be passed to the application as follows:

.. code:: python

    import quo

    kb = quo.keys.KeyBinder()
    app = quo.Suite(bind=kb)
    app.run()

To register a new keyboard shortcut, we can use the
:meth:`~quo.keys.KeyBinder.add` method as a decorator of
the key handler:

.. code:: python

    import quo

    bindings = quo.keys.KeyBinder()

    @bindings.add('ctrl-q')
    def exit_(event):
        """
        Pressing Ctrl-Q will exit the user interface.

        Setting a return value means: quit the event loop that drives the user
        interface and return this value from the `Suite.run()` call. 
        """
        event.app.exit()

    app = quo.Suite(bind=bindings, full_screen=True)
    app.run()

The callback function is named ``exit_`` for clarity, but it could have been
named ``_`` (underscore) as well, because we won't refer to this name.

:ref:`Read more about key bindings ...<bind>`


Modal containers
^^^^^^^^^^^^^^^^

The following container objects take a ``modal`` argument
:class:`~quo.layout.VSplit`,
:class:`~quo.layout.HSplit`, and
:class:`~quo.layout.FloatContainer`.

Setting ``modal=True`` makes what is called a **modal** container. Normally, a
child container would inherit its parent key bindings. This does not apply to
**modal** containers.

Consider a **modal** container (e.g. :class:`~quo.layout.VSplit`)
is child of another container, its parent. Any key bindings from the parent
are not taken into account if the **modal** container (child) has the focus.

This is useful in a complex layout, where many controls have their own key
bindings, but you only want to enable the key bindings for a certain region of
the layout.

The global key bindings are always active.


More about the Window class
---------------------------

As said earlier, a :class:`~quo.layout.Window` is a
:class:`~quo.layout.Container` that wraps a
:class:`~quo.layout.UIControl`, like a
:class:`~quo.layout.BufferControl` or
:class:`~quo.layout.FormattedTextControl`.

.. note::

    Basically, windows are the leafs in the tree structure that represent the UI.

A :class:`~quo.layout.Window` provides a "view" on the
:class:`~quo.layout.UIControl`, which provides lines of content. The
window is in the first place responsible for the line wrapping and scrolling of
the content, but there are much more options.

- Adding left or right margins. These are used for displaying scroll bars or
  line numbers.
- There are the `cursorline` and `cursorcolumn` options. These allow
  highlighting the line or column of the cursor position.
- Alignment of the content. The content can be left aligned, right aligned or
  centered.
- Finally, the background can be filled with a default character.


More about buffers and `BufferControl`
--------------------------------------



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
input, but it is possible to "merge" multiple processors into one with the
:func:`~quo.layout.processors.merge_processors` function.
[1]
