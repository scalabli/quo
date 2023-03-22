Table
======

``Printing tabular data``
--------------------------
:class:`quo.table.Table` function offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

**Parameters**

    - ``data`` - The first required argument. Can be a list-of-lists *(or another iterable of iterables)*, a list of named tuples, a dictionary of iterables, an iterable of dictionaries, a two-dimensional NumPy array, NumPy record array, or a Pandas' dataframe.
    - ``align`` - :class:`.WindowAlign` value or callable that return an :class:`.WindowAlign` value. alignment of content. i.e ``left``, ``centre`` or ``right``. ``centre`` is the default value.
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
  
 table = Table(data)
 
 table.print()

.. image:: https://raw.githubusercontent.com/scalabli/quo/master/docs/images/tables/table.png


``Table headers``
------------------

To print nice column headers, supply the ``headers`` argument.

- `headers` can be an explicit list of column headers.
- if `headers="firstrow"`, then the first row of data is used
- if `headers="keys"`, then dictionary keys or column indices are used otherwise a headerless table is produced.
  
.. code:: python

 from quo.table import Table
 
 data = [
    ["Name", "Gender", "Age"],
    ["Alice", "F", 24],
    ["Bob", "M", 19],
    ["Dave", "M", 24]
    ]
      
 table = Table(data)
 table.print(headers="firstrow")

``Column Widths and  Line Wrapping``
--------------------------------------
:func:`Table`  will, by default, set the width of each column to the length of the longest element in that column. However, in situations where fields are expected to reasonably be too long to look good as a single line, :param:`column_width` can help automate word wrapping long fields.

.. code:: python

 from quo.table import Table

 data = [
       [1, 'John Smith', 'This is a rather long description that might look better if it is wrapped a bit']
       ]

 table = Table(data)
 table.print(headers=("Issue Id", "Author", "Description"), column_width=[None, None, 30])


Right aligned table

.. code:: python

 from quo.table import Table
 
 data = [
    ["Name", "Gender", "Age"],
    ["Alice", "F", 24],
    ["Bob", "M", 19],
    ["Dave", "M", 24]
    ]

 table = Table(data)
 table.print(align="right")
 
    
 

.. image:: https://raw.githubusercontent.com/scalabli/quo/master/docs/images/tables/right-table.png

Colored table

.. code:: python

 from quo.table import Table
 
 data = [
    ["Name", "Gender", "Age"],
    ["Alice", "F", 24],
    ["Bob", "M", 19],
    ["Dave", "M", 24]
    ]
  
 table = Table(data)
 table.print(fg="green")
 

.. image:: https://raw.githubusercontent.com/scalabli/quo/master/docs/images/tables/green.png


Grid table

.. code:: python

 from quo.table import Table
 
 data = [
    ["Name", "Gender", "Age"],
    ["Alice", "F", 24],
    ["Bob", "M", 19],
    ["Dave", "M", 24]
    ]
    
 table = Table(data)
 table.print(theme="grid")
 
 
.. image:: https://raw.githubusercontent.com/scalabli/quo/master/docs/images/tables/grid.png
