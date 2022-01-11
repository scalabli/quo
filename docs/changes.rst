.. currentmodule:: quo


Changelog
==========
Version 2021.1.5
-----------------
Released on 2022-1-11
- ImportError: :issue:`37`

Version 2022.1
-----------------
Released on 2022-1-11
- Dependency update :issue:`32` to :issue:`35`
- TypeError: prompt() got an unexpected keyword argument :issue:`36`


Version 2021.7
--------------
Released on 2021-12-25

- Streamlined a number of features
- Fixed broken placeholder() issue :issue:`30`
- Faced out positional arguments ``foreground`` and ``background`` in favor of ``fg`` and ``bg``

Version 2021.6
---------------
Released on 2021-11-20

- Added Support of a placeholder text that is displayed as long as no input is given.
- Fixed minor bugs

Version 2021.5.5.2
------------------
Released on 2021-09-28

- Pypi README fix

Version 2021.5.5
-----------------

Released on 2021-09-23

- Added support for tabular presentation of data.

- Added support for colorful error messages

- Added parameter ``ul`` to ``echo`` function. Its the short form of the ``underline`` parameter

- Added a ``strike`` parameter to print strikethrough text.

- Added a ``hidden`` parameter to hide printed text


Version 2021.4.5
----------------

Released on 2021-08-22

- Phasing out module ``wcwidth`` to reduce the need for external dependencies.

- Intoducing the ``clipboard`` feature to copy and paste data flawlessly.



Version 2021.3.5
-----------------

Released on 2021-07-19

-   Added positional arguments `fg`` and ``bg`` which can still be used as a shortform of ``foreground`` and ``background``. foreground and background still works.

-   Added support for lively ``ProgressBars``

-   Implementation of :class: ``quo.text.HTML`` for easy text formating

-   Fixed changelong link on PyPI

-   Fixed wcwidth dependancy issue :issue:`18`
-   Added ability to display tabular which comes with several themes




Version 2021.2
-------------

Released on 2021-06-28

-   ``importlib_metadata`` backport package is installed on Python < 3.8 therefore will be be delisted as part of Quo's external dependency in later versions of Quo
-   Under the hood optimizations



Version 2021.1
---------------
Released on 2021-06-18

-   Added support for ``ANSI colors`` for better coloring of the terminal
-   Ability to Print both ``text`` and ``binary`` data to stdout 
-   Added support for RGB tuples of three integers
