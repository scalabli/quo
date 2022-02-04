Introduction
============
Quo is a Python based toolkit for writing Command-Line Interface(CLI) applications. Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API. Simple to code, easy to learn, and does not come with needless baggage.


Requirements
------------

Quo works flawlessly with Linux, OSX and Windows.

Quo requires Python ``3.8`` or later

Installation
------------

You can install Quo from PyPi with `pip`

```console

    pip install -U quo
```

Quick Start
-----------
```python
    import quo

    quo.echo(f"Hello World!", fg="red", italic=True, bold=True)
```

This will print ``"Hello World!"`` plus a new line to the terminal. Unlike the builtin print function, echo function has improved support for handling Unicode and binary data. If colorama is installed, the echo function will also support handling of ANSI color sequences.

