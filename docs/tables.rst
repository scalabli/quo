Tables
======

Here's an example:

..code-block:: python


    import quo

    table = [
     ["Name", "Gender", "Age"],
     ["Alice", "F", 24],
     ["Bob", "M", 19],
     ["Dave", "M", 24]
   ]

    quo.echo(quo.tabulate.tabular(table))
   
    
This produces the following output:

The :func:`~quo.tabulate.tabular` function offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

