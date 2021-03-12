.. rst-class:: hide-header

Quo
================

.. image:: _static/quo.png
    :align: center
    :scale: 33%
    :target: https://quo.rtfd.io

Quo is a Python  based module for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

Example1

.. code-block:: python

    import quo
    quo.echo(f'Hello Gerry') 


Example2:

.. code-block:: python

    import quo

    @quo.command()
    @quo.option('--count', default=2, help='The number of times the person is interviewed (n).')
    @quo.option('--name', prompt='Your name',
                  help='The name of the person to interview.')
    def hello(count, name):
        """Program that greets and interviews a person  for a total of 'n' times."""
        for x in range(count):
            quo.echo(f"Hello {name}!")

    if __name__ == '__main__':
        hello()


Quo in three points:

-   arbitrary nesting of commands
-   automatic help page generation
-   supports lazy loading of subcommands at runtime





You can get the library directly from PyPI::

    pip install quo

Documentation
-------------

This part of the documentation guides you through all of the library's
usage patterns.

.. toctree::
   :maxdepth: 2

   why
   quickstart
   setuptools
   parameters
   options
   arguments
   commands
   prompts
   documentation
   complex
   advanced
   testing
   utils
   shell-completion
   exceptions
   unicode-support
   wincmd

API Reference
-------------

Detailed guidelines on Quo's functionality

.. toctree::
   :maxdepth: 2

   api

Donate
------------
.. note:: Sponsoring our cause enables us to keep finding ways to contribute to communities, both in code/tools, and in community work. 

.. note:: `Donate <https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54>`_

.. toctree::
   :maxdepth: 2
   
   donate
   email
   twitter
   facebook
   

Miscellaneous Pages
-------------------

.. toctree::
   :maxdepth: 2

   contrib
   changelog
   upgrading
   license

