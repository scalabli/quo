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
     - ``body``    - Another container object.         - ``padding`` - The margin to be used around the body. This can be overriddenby :param:`padding_left`, :param:`padding_right`, :param:`padding_top` and :param:`padding_bottom` parameters.
     - ``style`` - A style string.
     - ``char``  - Character to be used for filling the space around the body. *(This is supposed tobe a character with a terminal width of 1.)*

.. code:: python

   https://github.com/secretum-inc/quo/src/master/examples/widgets/box/example1.py
