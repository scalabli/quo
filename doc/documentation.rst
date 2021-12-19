Documenting Scripts
===================

.. currentmodule:: quo

Quo makes it very easy to document your command line tools.  First of
all, it automatically generates help pages for you.  While these are
currently not customizable in terms of their layout, all of the text
can be changed.

Help Texts
----------

Commands and options accept help arguments.  In the case of commands, the
docstring of the function is automatically used if provided.

Simple example:

.. code-block:: python

    import quo

    @quo.command()
    @quo.app('--count', default=1, help='number of greetings')
    @quo.arg('name')
    def hello(count, name):
        """This script prints hello NAME COUNT times."""
        for x in range(count):
            quo.echo(f"Hello {name}!")




.. _documenting-arguments:

Documenting Arguments
~~~~~~~~~~~~~~~~~~~~~

:func:`quo.arg` does not take a ``help`` parameter. This is to
follow the general convention of Unix tools of using arguments for only
the most necessary things, and to document them in the command help text
by referring to them by name.

You might prefer to reference the argument in the description:

.. code-block:: python

    import quo

    @quo.command()
    @quo.arg('filename')
    def touch(filename):
        """Print FILENAME."""
        quo.echo(filename)


Or you might prefer to explicitly provide a description of the argument:

.. code-block:: python
    
    import quo

    @quo.command()
    @quo.arg('filename')
    def touch(filename):
        """Print FILENAME.

        FILENAME is the name of the file to check.
        """
        quo.echo(filename)


For more examples, see the examples in :doc:`/args`.


Preventing Rewrapping
---------------------

The default behavior of quo is to rewrap text based on the width of the
terminal.  In some circumstances, this can become a problem. The main issue
is when showing code examples, where newlines are significant.

Rewrapping can be disabled on a per-paragraph basis by adding a line with
solely the ``\b`` escape marker in it.  This line will be removed from the
help text and rewrapping will be disabled.

Example:

.. code-block:: python

    import quo

    @quo.command()
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


.. _doc-meta-variables:

Truncating Help Texts
---------------------

quo gets command help text from function docstrings.  However if you
already use docstrings to document function arguments you may not want
to see :param: and :return: lines in your help text.

You can use the ``\f`` escape marker to have quo truncate the help text
after the marker.

Example:

.. code-block:: python

    import quo
    
    @quo.command()
    @quo.pass_context
    def cli(clime):
        """First paragraph.

        This is a very long second
        paragraph and not correctly
        wrapped but it will be rewrapped.
        \f

        :param quo.core.Context clime: quo clime(context)
        """


Meta Variables
--------------

Apps and parameters accept a ``metavar`` argument that can change the
meta variable in the help page.  The default version is the parameter name
in uppercase with underscores, but can be annotated differently if
desired.  This can be customized at all levels:

.. code-block:: python

    import quo

    @quo.command(options_metavar='<options>')
    @quo.app('--count', default=1, help='number of greetings', metavar='<int>')
    @quo.arg('name', metavar='<name>')
    def hello(count, name):
        """This script prints hello <name> <int> times."""
        for x in range(count):
            quo.echo(f"Hello {name}!")



Command Short Help
------------------

For commands, a short help snippet is generated.  By default, it's the first
sentence of the help message of the command, unless it's too long.  This can
also be overridden:

.. code-block:: python

    import quo

    @quo.tether()
    def cli():
        """A simple command line tool."""
    @cli.command('init', short_help='init the repo')
    def init():
        """Initializes the repository."""
    @cli.command('delete', short_help='delete the repo')
    def delete():
        """Deletes the repository."""



Help Parameter Customization
-----------------------------
The help parameter is implemented in quo in a very special manner.
Unlike regular parameters it's automatically added by quo for any
command and it performs automatic conflict resolution.  By default it's
called ``--help``, but this can be changed.  If a command itself implements
a parameter with the same name, the default help parameter stops accepting
it.  There is a context setting that can be used to override the names of
the help parameters called :attr:`~Context.help_option_names`.

This example changes the default parameters to ``-h`` and ``--help``
instead of just ``--help``:

.. code-block:: python

    CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

    @quo.command(context_settings=CONTEXT_SETTINGS)
    def cli():
        pass

And what it looks like:

.. code-block:: python

    invoke(cli, ['-h'])
