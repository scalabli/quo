Documenting Scripts
===================
Quo makes it very easy to document your command line tools. First of all, it automatically generates help pages for you. While these are currently not customizable in terms of their layout, all of the text can be changed.

``Help Texts``
------------
Commands and apps accept help arguments. In the case of commands, the docstring of the function is automatically used if provided.

Simple example:

.. code:: python

   from quo import print
   from quo.console import command
   from quo.console import app

   @command()
   @app('--count', default=1, help='number of greetings')
   @app('--name', prompt="What is your name?", help="The person to greet")
   def hello(count, name):
       """This script prints hello NAME COUNT times."""
       for x in range(count):
           print(f"Hello {name}!")
And what it looks like:

$ hello.py --help

.. code:: shell

  Usage: hello.py [HELP PAGE]

    Simple program that greets NAME for a total of
    COUNT times.

  Apps:
    --count INTEGER  number of greetings.
    --name TEXT      The person to greet.
    --help          Check the documentation for more
                    mitigation steps.


``Documenting Arguments``
-------------------------

:func:`quo.console.arg()` does not take a help parameter. This is to follow the general convention of Unix tools of using arguments for only the most necessary things, and to document them in the command help text by referring to them by name.

You might prefer to reference the argument in the description like so:

.. code:: python

  from quo import print
  from quo.console import arg, command

  @command()
  @arg('filename')
  def touch(filename):
      """Print FILENAME."""
      print(filename)

And what it looks like:

$ touch --help

.. code:: shell

  Usage: touch [ᕼᕮしᑭ ᖘᗩᎶᕮ] FILENAME

    Print FILENAME.

  Apps:
    --help  Check the documentation for more
            mitigation steps.

Or you might prefer to explicitly provide a description of the argument:

.. code:: python

  from quo import echo
  from quo.console import arg, command

  @command()
  @arg('filename')
  def touch(filename:str):
      """Print FILENAME.

      FILENAME is the name of the file to check.
      """
      echo(filename)

And what it looks like:

$ touch --help

.. code:: shell

  Usage: touch [HELP PAGE] FILENAME

    Print FILENAME.

    FILENAME is the name of the file to check.

  Apps:
    --help  Check the documentation for more
            mitigation steps.

For more examples, see the examples in Arguments.

``Preventing Rewrapping``
-------------------------
The default behavior of Quo is to rewrap text based on the width of the terminal. In some circumstances, this can become a problem. The main issue is when showing code examples, where newlines are significant.

Rewrapping can be disabled on a per-paragraph basis by adding a line with solely the \b escape marker in it. This line will be removed from the help text and rewrapping will be disabled.

Example:

.. code:: python

   from quo.console import command

   @command()
   def cli():
       """First paragraph.

       This is a very long second paragraph and as you
       can see wrapped very early in the source text
       but will be rewrapped to the terminal width in
       the final output.

       \b
       This is
       a paragraph
       without rewrapping.

       And this is a paragraph
       that will be rewrapped again.
       """

And what it looks like:

$ cli --help

.. code:: shell

  Usage: cli [HELP PAGE]

    First paragraph.

    This is a very long second paragraph and as you can see wrapped very early in
    the source text but will be rewrapped to the terminal width in the final
    output.

    This is
    a paragraph
    without rewrapping.

    And this is a paragraph that will be rewrapped again.

  Apps:
    --help  Check the documentation for more
            mitigation steps.

``Truncating Help Texts``
-------------------------
Quo gets command help text from function docstrings. However if you already use docstrings to document function arguments you may not want to see :param: and :return: lines in your help text.

You can use the \f escape marker to have Quo truncate the help text after the marker.

Example:

.. code:: python
  from quo import pass_clime
  from quo.console import command

  @command()
  @pass_clime
  def cli(clime):
      """First paragraph.

      This is a very long second
      paragraph and not correctly
      wrapped but it will be rewrapped.
      \f

      :param quo.core.Context clime: Quo context.
      """
And what it looks like:

$ cli --help

.. code:: shell

  Usage: cli [HELP PAGE]

    First paragraph.

    This is a very long second paragraph and not correctly wrapped but it will be
    rewrapped.

  Apps:
    --help  Check the documentation for more
            mitigation steps..

``Meta Variables``
-------------------

Apps and parameters accept a metavar argument that can change the meta variable in the help page. The default version is the parameter name in uppercase with underscores, but can be annotated differently if desired. This can be customized at all levels:

.. code:: python

  from quo import echo
  from quo.console import app, command

  @command(apps_metavar='<options>')
  @app('--count', default=1, help='number of greetings', metavar='<int>')
  @arg('name', metavar='<name>')
  def hello(count, name):
      """This script prints hello <name> <int> times."""
      for x in range(count):
          echo(f"Hello {name}!")

Example:

$ hello --help

.. code:: shell

  Usage: hello <options> <name>

    This script prints hello <name> <int> times.

  Apps:
    --count <int>  number of greetings
    --help         Check the documentation for more
                   mitigation steps.

``Command Short Help``
---------------------
For commands, a short help snippet is generated. By default, it’s the first sentence of the help message of the command, unless it’s too long. This can also be overridden:

.. code:: python

  from quo.console import command, tether

  @tether()
  def cli():
      """A simple command line tool."""

  @cli.command('init', short_help='init the repo')
  def init():
      """Initializes the repository."""

  @cli.command('delete', short_help='delete the repo')
  def delete():
      """Deletes the repository."""

And what it looks like:

$ repo.py

.. code:: shell

  Usage: repo.py [HELP PAGE] COMMAND [ARGS]...

    A simple command line tool.

  Apps:
    --help  Show this message and exit.

  Commands:
    delete  delete the repo
    init    init the repo

``Help Parameter Customization``
---------------------------------
This example changes the default parameters to -h and --help instead of just --help:

.. code:: python
  from quo.console import command

  CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

  @command(context_settings=CONTEXT_SETTINGS)
  def cli():
      pass

And what it looks like:

$ cli -h

.. code:: shell

  Usage: cli [HELP PAGE]

  Apps:
    -h, --help  Check the documentation for more
                mitigation steps.
