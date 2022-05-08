.. currentmodule:: quo

Changelog
==========

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/master/docs/images/changelog.png

.. image:: https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif

``Version 2022.5.2``
---------------------

Released on 2022-05

**Added**
^^^^^^^^^^
- Added :func:`quo.color.Color`

``Version 2022.5.1``
---------------------

Released on 2022-05-07

**Fixed**
^^^^^^^^^^^
- Fixed :class:`SpinningWheel` attribute error.




``Version 2022.5``
--------------------

Released on 2022-05-01

**Added**
^^^^^^^^^^
- Added :meth:`quo.console.Console.spin`
- Added :param:`column_width` and :param:`headers` to :func:`quo.table.Table`
- Added :param:`suggest` to :class:`quo.prompt.Prompt`  
  
`Version 2022.4.5``
---------------------

Released on 2022-04-23

**Added**
^^^^^^^^^^
- Added :param:`case_sensitive` to :class:`quo.completion.WordCompleter`

  **Changed**
^^^^^^^^^^^^^
- Changed :param:`children` in class :class:`quo.layout.HSplit` to :param:`subset`
- Changed :param:`children` in class :class:`quo.layout.VSplit` to :param:`subset`
- Renamed :meth:`quo.console.Console.openfile` to :meth:`open`


``Version 2022.4.4``
-----------------------

Released on 2022-04-21

**Added**
^^^^^^^^^^^
- Added :param:`int` to :class:`quo.prompt.Prompt`
- Added :meth:`continuation` to :class:`quo.prompt.Prompt`


``Version 2022.4.3``
---------------------

Released on 2022-04-18

**Added**
^^^^^^^^^^^
- Added :param:`style` to :func:`quo.table.Table`
  

``Version 2022.4.2``
---------------------

Released on 2022-04-16

**Changed**
^^^^^^^^^^^^
- Under the hood optimization of class :class:`quo.progress.ProgressBar`

``Version 2022.4.1``
---------------------

Released on 2022-04-14

**Fixed**
^^^^^^^^^^



``Version 2022.4``
-------------------

Released on 2022-04-01

**Added**
^^^^^^^^^^

- Added :meth:`quo.console.Console.pager`
- Added :param:`fmt` to :func:`quo.print`
- Added :param:`bg` to all dialog boxes.
- Added :param:`multiline` to :func:`quo.dialog.InputBox`
- Added `TextField` as an aliase to :class:`TextArea`


``Version 2022.3.5``
--------------------

Released on 2022-03-19

**Changed**
^^^^^^^^^^^^
- Optimized :func:`quo.print`

``Version 2022.3.4``
---------------------

Released on 2022-03-18

**Added**
^^^^^^^^^^^
- Added :param:`bind` to :func:`quo.container`
- Added :param:`focused_element` to :func:`quo.container`
- Added :param:`full_screen` to :func:`quo.container`
- Added :param:`mouse_support` to :func:`quo.container`
- Added :param:`refresh` to :func:`quo.container`
- Added :func:`quo.keys.bind` as an instance of :obj:`quo.keys.Bind`
- Added :func:`quo.console.console` as an instance of :obj:`quo.console.Console`

``Version 2022.3.3``
---------------------

Released on 2022-03-16

**Changed**
^^^^^^^^^^^^
- Optimized :param:`align` in :class:`quo.layout.Window`, :class:`quo.layout.HSplit` and :class:`quo.layout.VSplit`



``Version 2022.3.2``
----------------------

Released on 2022-3-14

**Added**
^^^^^^^^^^
- Added :meth:`quo.console.Console.bar`
- Added :meth:`qquo.console.Console.rule`

**Changed**
^^^^^^^^^^^^^
- Deprecated :param:`.run()` in the Dialog UI.

``Version 2022.3.1``
---------------------

Released on 2022-3-12

**Added**
^^^^^^^^^^^
- Added :param:`ul` as an alias of :param:`underline` for :class:`~quo.style.Style`.

``Version 2022.3``
--------------------

Released on 2022-3-6

**Added**
^^^^^^^^^^
- Added key binder :kbd:`<any>` enabling the user to press any key to exit the help page.
- Introduced :class:`quo.keys.Bind` as an alias of :class:`quo.keys.KeyBinder`

**Changed**
^^^^^^^^^^^^
- Changed :param:`enable_system_elicit` in favor of :param:`system_prompt`.
- Changed :param:`enable_suspend` in favor of :param:`suspend`.

**Fixed**
^^^^^^^^^^
- Optimized the help page.
- Fixed Deprecated notice `TypeError`


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
- Fixed :func:`quo.Console.edit`, :func:`quo.Console.openfile`, :func:`quo.Console.encoding`

 ``Version 2022.2``
-------------------

Released on 2022-2-16

**Added**
^^^^^^^^^^
- Added :func:`quo.Console.edit`
- Added :func:`quo.Console.launch`
- Added :func:`quo.Console.size`
- Added :func:`quo.Console.encoding`
- Added :func:`quo.Console.bell`                                - Added :func:`quo.Console.rule`
- Added :func:`quo.Console.openfile`
- Added :func:`quo.types.integer`

**Changed**
^^^^^^^^^^^^^
- Deprecated :param:`password` in favor of :param:`hide`
- Deprecated :class:`quo.text.HTML` in favor of :class:`quo.text.Text`
- Deprecated :param:`r_elicit` in favor of :param:`rprompt`
- Deprecated :class:`quo.Suite` in favor of :class:`quo.console.Console`
- Deprecated :param:`validator` in favor of :param:`type`
- Dropped support for `python < 3.8`

**Fixed**
^^^^^^^^^^
- Full support for Windows

``Version 2022.1.6``
---------------------
Released on 2022-1-17

- Under the hood optimizations
- Introduced :func:`quo.dialog.MessageBox`, :func:`quo.dialog.PromptBox`, :func:`quo.dialog.RadiolistBox`, :func:`quo.dialog.ConfirmBox`, :func:`quo.dialog.CheckBox`, :func:`quo.dialog.ChoiceBox` widgets for displaying formatted text in a window.

``Version 2022.1.5``
---------------------
Released on 2022-1-11

**Fixed**
^^^^^^^^^^
- ImportError: :issue:`37` affecting Windows OS

``Version 2022.1``
-------------------
Released on 2022-1-11

**Changed**
^^^^^^^^^^^^
- Dependency update :issue:`32` to :issue:`35`

**Fixed**
^^^^^^^^^^
- Unexpected argument in :func:`quo.prompt()` :issue:`36`

``Version 2021.7``
-------------------
Released on 2021-12-25

**Changed**
^^^^^^^^^^^^^
- Deprecated :param:`foreground` and :param:`background`` in favor of :param:`fg` and :param:`bg`

**Fixed**
^^^^^^^^^^^
- Fixed broken placeholder() issue :issue:`30`

``Version 2021.6``
-------------------
Released on 2021-11-20

**Added**
^^^^^^^^^^^
- Added Support of a placeholder text that is displayed as long as no input is given.

``Version 2021.5.5.2``
----------------------
Released on 2021-09-28

**Fixed**
^^^^^^^^^^
- Pypi README fix

``Version 2021.5.5``
---------------------

Released on 2021-09-2

**Added**
^^^^^^^^^^^
- Added support for tabular presentation of data.
- Added support for colorful error messages.
- Added :param:`ul` to :func:`quo.echo`. Can be used as a substitute for :param:`underline`  parameter.
- Added :param:`strike`` to :func:`quo.echo`
- Added a :param:`hidded` to :func:`quo.echo`


``Version 2021.4.5``
--------------------

Released on 2021-08-22

**Added**
^^^^^^^^^^^
- Intoduced :class:`quo.clipboard.InMemoryClipboard` class to copy and paste data flawlessly.


``Version 2021.3.5``
---------------------

Released on 2021-07-19

**Added**
^^^^^^^^^^^
- Added :param:`fg` and :param:`bg` as an alias of :param:`foreground` and :param:`background`.
- Added :class:`quo.progress.ProgressBar` class.
- Added :class:`quo.text.HTML` for easy text formating.

**Changed**
^^^^^^^^^^^^
- Fixed changelong link on PyPI.
- Fixed wcwidth dependancy issue :issue:`18`



``Version 2021.2``
-------------------

Released on 2021-06-28

- Under the hood optimizations.



``Version 2021.1``
-------------------

Released on 2021-06-18

**Added**
^^^^^^^^^^^
- Added support for ``ANSI colors`` for better coloring of the terminal
- Added support for RGB tuples of three integers


      *****

``Version 2021.1.dev0``
-------------------------

Released on 2021-01-10

- Proof of concept
