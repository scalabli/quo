.. _rendering_flow:

The rendering flow
==================

Understanding the rendering flow is important for understanding how
:class:`~quo.layout.Container` and
:class:`~quo.layout.UIControl` objects interact. We will demonstrate
it by explaining the flow around a
:class:`~quo.layout.BufferControl`.

.. note::

    A :class:`~quo.layout.BufferControl` is a
    :class:`~quo.layout.UIControl` for displaying the content of a
    :class:`~quo.buffer.Buffer`. A buffer is the object that holds
    any editable region of text. Like all controls, it has to be wrapped into a
    :class:`~quo.layout.Window`.

Let's take the following code:

.. code:: python

    from quo.enums import DEFAULT_BUFFER
    from quo.layout.containers import Window
    from quo.layout.controls import BufferControl
    from quo.buffer import Buffer

    b = Buffer(name=DEFAULT_BUFFER)
    Window(content=BufferControl(buffer=b))

What happens when a :class:`~quo.renderer.Renderer` objects wants a
:class:`~quo.layout.Container` to be rendered on a certain
:class:`~quo.layout.screen.Screen`?

The visualisation happens in several steps:

1. The :class:`~quo.renderer.Renderer` calls the
   :meth:`~quo.layout.Container.write_to_screen` method
   of a :class:`~quo.layout.Container`.
   This is a request to paint the layout in a rectangle of a certain size.

   The :class:`~quo.layout.Window` object then requests
   the :class:`~quo.layout.UIControl` to create a
   :class:`~quo.layout.UIContent` instance (by calling
   :meth:`~quo.layout.UIControl.create_content`).
   The user control receives the dimensions of the window, but can still
   decide to create more or less content.

   Inside the :meth:`~quo.layout.UIControl.create_content`
   method of :class:`~quo.layout.UIControl`, there are several
   steps:

   2. First, the buffer's text is passed to the
      :meth:`~quo.highlight.Lexer.lex_document` method of a
      :class:`~quo.highlight.Lexer`. This returns a function which
      for a given line number, returns a "formatted text list" for that line
      (that's a list of ``(style_string, text)`` tuples).

   3. This list is passed through a list of
      :class:`~quo.layout.processors.Processor` objects.
      Each processor can do a transformation for each line.
      (For instance, they can insert or replace some text, highlight the
      selection or search string, etc...)

   4. The :class:`~quo.layout.UIControl` returns a
      :class:`~quo.layout.UIContent` instance which
      generates such a token lists for each lines.

The :class:`~quo.layout.Window` receives the
:class:`~quo.layout.UIContent` and then:

5. It calculates the horizontal and vertical scrolling, if applicable
   (if the content would take more space than what is available).

6. The content is copied to the correct absolute position
   :class:`~quo.layout.screen.Screen`, as requested by the
   :class:`~quo.renderer.Renderer`. While doing this, the
   :class:`~quo.layout.Window` can possible wrap the
   lines, if line wrapping was configured.

Note that this process is lazy: if a certain line is not displayed in the
:class:`~quo.layout.Window`, then it is not requested
from the :class:`~quo.layout.UIContent`. And from there, the line is
not passed through the processors or even asked from the
:class:`~quo.highlight.Lexer`.
