Documenting Scripts
===================
Quo makes it very easy to document your command line tools. First of all, it automatically generates help pages for you. While these are currently not customizable in terms of their layout, all of the text can be changed.

Help Texts
Commands and apps accept help arguments. In the case of commands, the docstring of the function is automatically used if provided.

Simple example:

.. code:: python

  import quo

   @quo.command()
   @quo.app('@count', default=1, help='number of greetings')
   @quo.arg('name')
   def hello(count, name):
       """This script prints hello NAME COUNT times."""
       for x in range(count):
           quo.echo(f"Hello {name}!")
And what it looks like:

.. code:: console
$ hello --help
Usage: hello [ᕼᕮしᑭ ᖘᗩᎶᕮ] NAME

  This script prints hello NAME COUNT times.

Apps:
  @count INTEGER  number of greetings
  --help           Show this message and exit.
Documenting Arguments
click.argument() does not take a help parameter. This is to follow the general convention of Unix tools of using arguments for only the most necessary things, and to document them in the command help text by referring to them by name.

You might prefer to reference the argument in the description:

@click.command()
@click.argument('filename')
def touch(filename):
    """Print FILENAME."""
    click.echo(filename)
And what it looks like:

$ touch --help
Usage: touch [OPTIONS] FILENAME

  Print FILENAME.

Options:
  --help  Show this message and exit.
Or you might prefer to explicitly provide a description of the argument:

@click.command()
@click.argument('filename')
def touch(filename):
    """Print FILENAME.

    FILENAME is the name of the file to check.
    """
    click.echo(filename)
And what it looks like:

$ touch --help
Usage: touch [OPTIONS] FILENAME

  Print FILENAME.

  FILENAME is the name of the file to check.

Options:
  --help  Show this message and exit.
For more examples, see the examples in Arguments.

Preventing Rewrapping
The default behavior of Click is to rewrap text based on the width of the terminal. In some circumstances, this can become a problem. The main issue is when showing code examples, where newlines are significant.

Rewrapping can be disabled on a per-paragraph basis by adding a line with solely the \b escape marker in it. This line will be removed from the help text and rewrapping will be disabled.

Example:

@click.command()
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
Usage: cli [OPTIONS]

  First paragraph.

  This is a very long second paragraph and as you can see wrapped very early in
  the source text but will be rewrapped to the terminal width in the final
  output.

  This is
  a paragraph
  without rewrapping.

  And this is a paragraph that will be rewrapped again.

Options:
  --help  Show this message and exit.
Truncating Help Texts
Click gets command help text from function docstrings. However if you already use docstrings to document function arguments you may not want to see :param: and :return: lines in your help text.

You can use the \f escape marker to have Click truncate the help text after the marker.

Example:

@click.command()
@click.pass_context
def cli(ctx):
    """First paragraph.

    This is a very long second
    paragraph and not correctly
    wrapped but it will be rewrapped.
    \f

    :param click.core.Context ctx: Click context.
    """
And what it looks like:

$ cli --help
Usage: cli [OPTIONS]

  First paragraph.

  This is a very long second paragraph and not correctly wrapped but it will be
  rewrapped.

Options:
  --help  Show this message and exit.
Meta Variables
Options and parameters accept a metavar argument that can change the meta variable in the help page. The default version is the parameter name in uppercase with underscores, but can be annotated differently if desired. This can be customized at all levels:

@click.command(options_metavar='<options>')
@click.option('--count', default=1, help='number of greetings',
              metavar='<int>')
@click.argument('name', metavar='<name>')
def hello(count, name):
    """This script prints hello <name> <int> times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
Example:

$ hello --help
Usage: hello <options> <name>

  This script prints hello <name> <int> times.

Options:
  --count <int>  number of greetings
  --help         Show this message and exit.
Command Short Help
For commands, a short help snippet is generated. By default, it’s the first sentence of the help message of the command, unless it’s too long. This can also be overridden:

@click.group()
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
Usage: repo.py [OPTIONS] COMMAND [ARGS]...

  A simple command line tool.

Options:
  --help  Show this message and exit.

Commands:
  delete  delete the repo
  init    init the repo
Help Parameter Customization
Changelog
The help parameter is implemented in Click in a very special manner. Unlike regular parameters it’s automatically added by Click for any command and it performs automatic conflict resolution. By default it’s called --help, but this can be changed. If a command itself implements a parameter with the same name, the default help parameter stops accepting it. There is a context setting that can be used to override the names of the help parameters called help_option_names.

This example changes the default parameters to -h and --help instead of just --help:

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    pass
And what it looks like:

$ cli -h
Usage: cli [OPTIONS]

Options:
  -h, --help  Show this message and exit.
Sponsored: EthicalAds
Generate revenue while preserving user-privacy. Start earning today by hosting EthicalAds
Ad by EthicalAds   ·   Monetize your site
Contents
Documenting Scripts
Help Texts
Documenting Arguments
Preventing Rewrapping
Truncating Help Texts
Meta Variables
Command Short Help
Help Parameter Customization
Navigation
Overview
Previous: User Input Prompts
Next: Complex Applications
Quick search
© Copyright 2014 Pallets. Created using Sphinx 4.3.2.
  v: 8.0.x 
