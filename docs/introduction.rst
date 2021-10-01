Introduction
============
Quo is a Python based toolkit for writing Command-Line Interface(CLI) applications. Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API. Simple to code, easy to learn, and does not come with needless baggage.


Requirements
------------

Quo works flawlessly with Linux, OSX and Windows.

Quo requires Python ``3.6.1`` or later

.. note::
    PyCharm users will need to enable "emulate terminal" in output console option in run/debug configuration to see styled output.

Installation
------------

You can install Quo from PyPi with `pip`

.. code-block:: console

    pip install -U quo

If you intend to use Rich with Jupyter then there are some additional dependencies which you can install with the following command::

    pip install rich[jupyter]


Quick Start
-----------
.. code-block:: python

    from quo import echo

    echo(f"Hello World!", fg="red", italic=True, bold=True)

This will print ``"Hello World!"`` plus a new line to the terminal. Unlike the builtin print function, echo function has improved support for handling Unicode and binary data. If colorama is installed, the echo function will also support handling of ANSI color sequences.

