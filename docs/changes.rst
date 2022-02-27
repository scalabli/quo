.. currentmodule:: quo

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/master/docs/images/changelog.png

.. image:: https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif

Changelog
=========

``Version 2022.3``
--------------------

Unreleased

**Fixed**
^^^^^^^^^
- Optimized the help parameter.

**Added**
----------
Introduced :class:`quo.keys.Bind` as an alias of :class:`quo.keys.KeyBinder`

``Version 2022.2.2``
--------------------

Released on 2022-2-2

**Added**
^^^^^^^^^^
- Added :func:`quo.console.command`
- Added :func:`quo.console.app`
- Added :func:`quo.console.arg`
- Added :func:`quo.console.tether`
- Added highlighters : `Actionscript`, `Arrow`, `Bibtex`, `Cpp`, `Css`, `Email, Fortran, Go, Haskell, HTML, Javascript,  Julia, Perl, Php, Python, Ruby, Rust, Shell, Solidity, Sql`

**Fixed**
^^^^^^^^^^
- Under the hood optimizations.

``Version 2022.2.1``
---------------------

Released on 2022-2-25

**Changed**
^^^^^^^^^^^^
- Deprecated :param:`is_password` in favor of :param:`hide`
  
**Fixed**
^^^^^^^^^^
- Fixed :func:`quo.Console.edit`, :func:`quo.Console.rule`, :func:`quo.Console.openfile`, :func:`quo.Console.encoding`

 ``Version 2022.2``
-------------------

Released on 2022-2-16

- Fixed minor bugs
- Added :func:`quo.types.integer`
- Deprecated :param:`password` in favor of :param:`hide`
- Deprecated :class:`quo.text.HTML` in favor of :class:`quo.text.Text`
- Deprecated :param:`r_elicit` in favor of :param:`rprompt`
- Deprecated :class:`quo.Suite` in favor of :class:`quo.Console`
- Deprecated :param:`validator` in favor of :param:`type`
- Added :func:`quo.Console.edit`
- Added :func:`quo.Console.launch`
- Added :func:`quo.Console.size`
- Added :func:`quo.Console.encoding`
- Added :func:`quo.Console.bell`
- Added :func:`quo.Console.rule`
- Added :func:`quo.Console.openfile`
- Full support for Windows
- Dropped support for `python < 3.8`


``Version 2022.1.6``
---------------------
Released on 2022-1-17

- Under the hood optimizations
- Introduced :func:`quo.MessageBox`, :func:`quo.PromptBox`, :func:`quo.RadiolistBox`, :func:`quo.ConfirmationBox`, :func:`quo.CheckBox`, :func:`quo.ChoiceBox` widgets for displaying formatted text in a window.

``Version 2022.1.5``
---------------------
Released on 2022-1-11

- ImportError: :issue:`37` affecting Windows OS

``Version 2022.1``
-------------------
Released on 2022-1-11

- Dependency update :issue:`32` to :issue:`35`
- Unexpected argument in :func:`quo.prompt()` :issue:`36`


``Version 2021.7``
-------------------
Released on 2021-12-25

- Streamlined a number of features
- Fixed broken placeholder() issue :issue:`30`
- Deprecated :param:`foreground` and :param:`background`` in favor of :param:`fg` and :param:`bg`

``Version 2021.6``
-------------------
Released on 2021-11-20

- Added Support of a placeholder text that is displayed as long as no input is given.
- Fixed minor bugs

``Version 2021.5.5.2``
----------------------
Released on 2021-09-28

- Pypi README fix

``Version 2021.5.5``
---------------------

Released on 2021-09-23

- Added support for tabular presentation of data.

- Added support for colorful error messages

- Added :param:`ul` to :func:`quo.echo`. Can be used as a substitute for :param:`underline`  parameter.

- Added a ``strike`` parameter to print strikethrough text.

- Added a ``hidden`` parameter to hide printed text


``Version 2021.4.5``
--------------------

Released on 2021-08-22

- Phasing out module ``wcwidth`` to reduce the need for external dependencies.

- Intoducing the ``clipboard`` feature to copy and paste data flawlessly.



``Version 2021.3.5``
---------------------

Released on 2021-07-19

-   Added positional arguments `fg`` and ``bg`` which can still be used as a shortform of ``foreground`` and ``background``. foreground and background still works.

-   Added support for lively ``ProgressBars``

-   Implementation of :class: ``quo.text.HTML`` for easy text formating

-   Fixed changelong link on PyPI

-   Fixed wcwidth dependancy issue :issue:`18`
-   Added ability to display tabular which comes with several themes




``Version 2021.2``
-------------------

Released on 2021-06-28

-   ``importlib_metadata`` backport package is installed on Python < 3.8 therefore will be be delisted as part of Quo's external dependency in later versions of Quo
-   Under the hood optimizations



``Version 2021.1``
-------------------

Released on 2021-06-18

-   Added support for ``ANSI colors`` for better coloring of the terminal
-   Ability to Print both ``text`` and ``binary`` data to stdout 
-   Added support for RGB tuples of three integers
