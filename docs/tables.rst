Tables
======

Rich's :class:`~rich.table.Table` class offers a variety of ways to render tabular data to the terminal.

To render a table, construct a :class:`~rich.table.Table` object, add columns with :meth:`~rich.table.Table.add_column`, and rows with :meth:`~rich.table.Table.add_row` -- then print it to the console.

Here's an example:

..code-block:: python

    from quo import echo
    from quo.tabulate import tabular
    
    table = [
     ["Name", "Gender", "Age"],
     ["Alice", "F", 24],
     ["Bob", "M", 19],
     ["Dave", "M", 24]
   ]
   
   echo(tabular(table))
   
    
This produces the following output:

The :func:`~quo.tabulate.tabular` function offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

