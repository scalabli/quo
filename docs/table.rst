Table
======

``Printing tabular data``
--------------------------
:func:`quo.table.Table` function offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

.. code:: python

  from quo.table import Table
  
  example = [
  ["Name", "Gender", "Age"],
  ["Alice", "F", 24],
  ["Bob", "M", 19],
  ["Dave", "M", 24]
  ]
  print(Table(example))
