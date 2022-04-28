Table
======

``Printing tabular data``
--------------------------
:class:`quo.table.Table` function offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

**Parameters**

    - ``data`` - The first required argument. Can be a list-of-lists *(or another iterable of iterables)*, a list of named tuples, a dictionary of iterables, an iterable of dictionaries, a two-dimensional NumPy array, NumPy record array, or a Pandas' dataframe.
    - ``align`` - :class:`.WindowAlign` value or callable that return an :class:`.WindowAlign` value. alignment of content. i.e ``left``, ``centre`` or ``right``
    - ``style`` - A style string.

   - ``theme``  -  **plain** - Separates columns with a double space.
               -  **simple** - like Pandoc simple_tables.
               -  **grid** - similar to tables produced by Emacs table.el package.
               -  **fancy_grid** - *(Default theme)* draws a grid using box-drawing characters.
               -  **pipe** - Like tables in PHP Markdown Extra extension.
               -  **orgtbl** - Like tables in Emacs org-mode and orgtbl-mode.
               -  **latex** - Produces a tabular environment of LaTeX document markup.
               -  **presto** - Like tables produce by the Presto CLI.
               -  **mediawiki** - Produces a table markup used in Wikipedia and on other MediaWiki-based sites.
               -  **rst** - Like a simple table format from reStructuredText.


Changed on *v2022.4.3*

.. code:: python

 from quo.table import Table
  
 data = [
 ["Name", "Gender", "Age"],
 ["Alice", "F", 24],
 ["Bob", "M", 19],
 ["Dave", "M", 24]
 ]

 Table(data)

.. image:: https://raw.githubusercontent.com/scalabli/quo/master/docs/images/table.png
