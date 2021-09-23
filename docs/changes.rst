.. currentmodule:: quo


Changelog
=========

Version 2021.5.5
-----------------

2021-09-23

- Added support for tabular presentation of data.

- Added support for colorful error messages

- Added parameter ``ul`` to ``echo`` function. Its the short form of the ``underline`` parameter

- Added a ``strike`` parameter to print strikethrough text.

- Added a ``hidden`` parameter to hide printed text


Version 2021.4.5
----------------

2021-08-22

- Phasing out module ``wcwidth`` to reduce the need for external dependencies.

- Intoducing the ``clipboard`` feature to copy and paste data flawlessly.



Version 2021.3.5
-----------------

2021-07-19

-   Added ``fg`` and ``bg`` which can still be used as a shortform of ``foreground`` and ``background``. foreground and background still works.

-   Added support for lively ``ProgressBars``

-   Minimal implementation of ``HTML`` module to easy formating

-   Fixed changelong link on PyPI

-   Fixed wcwidth dependancy issue :issue:`18`
-   Added ability to display tabular which comes with several themes/formats
-
-



Version 2021.2
-------------

Released 2021-06-28

-   ``importlib_metadata`` backport package is installed on Python < 3.8 therefore will be be delisted as part of Quo's external dependency in later versions of Quo
-
-
-
-
-


Version 2021.1
---------------
Released 2021-06-18
`
-   Added support for ``ANSI colors`` for better coloring of the terminal
-   Ability to Print both ``text`` and ``binary`` data to stdout 
-   Added support for RGB tuples of three integers
-
-
-
-
-
