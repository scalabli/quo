

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/main/pics/quo.png

===========================
 Quo
===========================

|coverage| |license| |wheel| |pyimp| |RTD| |PyPI| |PyStats|

:Version: 2021.4.5
:Web: http://quo.readthedocs.io/
:Download: http://pypi.org/project/quo
:Source: http://github.com/secretum-inc/quo


.. sourcecode:: python

    # Quo
    # Forever scalable

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.
Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API.
Simple to code, easy to learn, and does not come with needless baggage. 

Quo requires Python `3.6.1` or later. 

Installation
============
You can install quo via the Python Package Index (PyPI)

.. sourcecode:: console

    $ pip install -U quo


Getting Started
================
The most simple examples of would look like this:

**Example 1**

.. sourcecode:: python

    import quo
    quo.echo(f'Hello, World!')
    

**Example 2**

.. sourcecode:: python

  from quo import echo
  echo(f'Hello, World!', fg="red", bold=True)

**Example 3**

.. sourcecode:: python

   from quo import echo
   echo(f"Hello, World in italics!", italic=True)


**Example 4**

.. sourcecode:: python

   from quo import echo, prompt
   answer = prompt("How old are you?")
   echo(f"I am: {answer}")


**Example 5**

.. sourcecode:: python

   from quo import command, app, echo                                                                  
   
   @command()
   @app("--name", prompt="What is your name?", type=str)
   @app("--age", prompt="How old are you?", type=int)
   def hello(name, age):
        echo(f"Hello {name}, nice to meet ya")
        echo(f"{name}, {age} is not that bad")

**Example 6**

.. sourcecode:: python

  from quo import container, Frame, TextArea
  container(
    Frame(
    TextArea(text="Hello world!\n"),
    title="Quo: ♥", )
    )


For more intricate  examples, have a look in the ``tutorials`` directory and the documentation.

Features
==========
- Support for ANSI and RGB color models
- Support for tabular presentation of data
- Interactive progressbars
- Nesting of commands
- A function that displays asterisks instead of the actual characters, helpful when typing passwords
- Automatic help page generation
- Lightweight


Donate🎁
=========

In order to for us to maintain this project and grow our community of contributors, `please consider donating today`_.

.. _please consider donating today: https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54



Quo is...
===========

**Simple**
     If you know Python you can  easily use quo and it can integrate with just about anything.




Getting Help
=============

.. _gitter-channel:

Gitter
-------

For discussions about the usage, development, and future of quo,
please join our Gitter community

* https://gitter.im/secretum-inc
* Join: https://gitter.im/secretum-inc/quo

Resources
==========

.. _bug-tracker:

Bug tracker
------------

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at https://github.com/secretum-inc/quo/issues/

.. _license:

License📑
==========

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.


Code of Conduct
================
Code of Conduct is adapted from the Contributor Covenant,
version 1.2.0 available at http://contributor-covenant.org/version/1/2/0/.

.. |build-status| image:: https://pepy.tech/badge/quo/month
    :alt: Downloads
    :target: https://pepy.tech/badge/quo/month

.. |coverage| image:: https://snyk.io/advisor/python/quo/badge.svg
    :alt: Package Health
    :target: https://snyk.io/advisor/python/quo

.. |license| image:: https://img.shields.io/pypi/l/quo.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT

.. |wheel| image:: https://img.shields.io/pypi/wheel/quo.svg
    :alt: quo can be installed via wheel
    :target: http://pypi.org/project/quo/

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/quo.svg
    :alt: Supported Python versions.
    :target: http://pypi.org/project/quo/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/quo.svg
    :alt: Support Python implementations.
    :target: http://pypi.org/project/quo/

.. |RTD| image:: https://readthedocs.org/projects/quo/badge/
    :target: https://quo.readthedocs.io/

.. |PyPI| image:: https://img.shields.io/pypi/v/quo.svg
    :target: https://pypi.python.org/pypi/quo/
    :alt: Latest Version

..  |PyStats| image:: https://static.pepy.tech/personalized-badge/quo?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads
 :target: https://pepy.tech/project/quo
