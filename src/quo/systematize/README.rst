Systematize
=============




tabular
===============

Print tabular data in Python!!

rinting small tables without hassle: just one function call,
    formatting is guided by the data itself
-   authoring tabular data for lightweight plain-text markup: multiple
    output formats suitable for further editing or transformation
-   readable presentation of mixed textual and numeric data: smart
    column alignment, configurable number formatting, alignment by a
    decimal point




## Table themes

There is more than one way to format a table in plain text. The third
optional argument named `theme` defines how the table is formatted.

Here's a list of supported themes:

-   "plain"
-   "simple"
-   "github"
-   "grid"
-   "fancy_grid"
-   "pipe"
-   "orgtbl"
-   "jira"
-   "presto"
-   "pretty"
-   "psql"
-   "rst"
-   "mediawiki"
-   "moinmoin"
-   "youtrack"
-   "html"
-   "unsafehtml"
-   "latex"
-   "latex_raw"
-   "latex_booktabs"
-   "latex_longtable"
-   "textile"
-   "tsv"

`plain` tables do not use any pseudo-graphics to draw lines:


`fancy_grid` is the default theme, itdraws a grid using box-drawing characters:

.. code:: python

   import quo
   from quo import echo, tabular
   table = [["U.S.A",42],["U.K",451],["Kenya",20]]
   headers = ["Countries", "qty"]

   echo(tabular(table, headers))
    ╒════════╤═══════╕
    │Country │   qty │
    ╞════════╪═══════╡
    │ U.S.A  │    42 │
    ├────────┼───────┤
    │ U.K    │   451 │
    ├────────┼───────┤
    │ Kenya  │   20  │
    ╘════════╧═══════╛

`presto` theme:

.. code:: python

    import quo
    from quo import echo, tabular
    table = [["U.S.A",42],["U.K",451],["Kenya",20]]
    headers = ["Countries", "qty"]
    
    echo(tabular(table, headers, theme="presto"))
            | 
     Country|  qty
    --------+-------
     U.S.A  |   42
     U.K    |   451
     Kenya  |    2

Feel free to check out other themes
