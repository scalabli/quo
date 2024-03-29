.. _arguments:

Args
=========

.. currentmodule:: quo

Args work similarly to :ref:`apps <apps>` but are positional.
They also only support a subset of the features ofapps  due to their syntactical nature.

``Basic Args``
---------------

The most basic option is a simple string arg of one value.  If no
type is provided, the type of the default value is used, and if no default
value is provided, the type is assumed to be :data:`STRING`.

.. code:: python

 from quo import echo
 from quo.console import arg, command

 @command()
 @arg('filename')
 def touch(filename):
     """Print FILENAME."""
     echo(filename)


``Variadic Args``
------------------

The second most common version is variadic args where a specific (or
unlimited) number of args is accepted.  This can be controlled with
the ``nargs`` parameter.  If it is set to ``-1``, then an unlimited number
of args is accepted.

The value is then passed as a tuple.  Note that only one argument can be
set to ``nargs=-1``, as it will eat up all args.

Example

.. code:: python

     from quo import echo
     from quo.console import arg, command

     @command()
     @arg('src', nargs=-1)
     @arg('dst', nargs=1)
     def copy(src, dst):
        """Move file SRC to DST."""
        for fn in src:
            echo(f"move {fn} to folder {dst}")


Note that this is not how you would write this application.  The reason
for this is that in this particular example the arguments are defined as
strings.  Filenames, however, are not strings!  They might be on certain
operating systems, but not necessarily on all.  For better ways to write
this, see the next sections.
 

.. _file-args:

``File Arguments``
-------------------

Since all the examples have already worked with filenames, it makes sense
to explain how to deal with files properly.  Command line tools are more
fun if they work with files the Unix way, which is to accept ``-`` as a
special file that refers to stdin/stdout.

quo supports this through the :class:`quo.types.File` type which handles files for you.  It also deals with Unicode and bytes.

Example:

.. code:: python

    from quo.console import arg, command
    from quo.types import File

    @command()
    @arg('input', type=File('rb'))
    @arg('output', type=File('wb'))
    def inout(input, output):
        """Copy contents of INPUT to OUTPUT."""
        while True:
            chunk = input.read(1024)
            if not chunk:
                break
            output.write(chunk)


``File Path Args``
-------------------

In the previous example, the files were opened immediately.  But what if
we just want the filename?  The naïve way is to use the default string
argument type.  However, remember that quo is Unicode-based, so the string
will always be a Unicode value.  Unfortunately, filenames can be Unicode or
bytes depending on which operating system is being used.  As such, the type
is insufficient.

Instead, you should be using the :class:`Path` type, which automatically
handles this ambiguity.  Not only will it return either bytes or Unicode
depending on what makes more sense, but it will also be able to do some
basic checks for you such as existence checks.

Example:

.. code:: python

    from quo import echo, formatfilename
    from quo.console import arg, command
    from quo.types import Path

    @command()
    @arg('filename', type=Path(exists=True))
    def touch(filename):
        """Print FILENAME if the file exists."""
        echo(formatfilename(filename))


``File Opening Safety``
-----------------------

The :class:`FileType` type has one problem it needs to deal with, and that
is to decide when to open a file.  The default behavior is to be
"intelligent" about it.  What this means is that it will open stdin/stdout
and files opened for reading immediately.  This will give the user direct
feedback when a file cannot be opened, but it will only open files
for writing the first time an IO operation is performed by automatically
wrapping the file in a special wrapper.

This behavior can be forced by passing ``lazy=True`` or ``lazy=False`` to
the constructor.  If the file is opened lazily, it will fail its first IO
operation by raising an :exc:`FileError`.

Since files opened for writing will typically immediately empty the file,
the lazy mode should only be disabled if the developer is absolutely sure
that this is intended behavior.

Forcing lazy mode is also very useful to avoid resource handling
confusion.  If a file is opened in lazy mode, it will receive a
``close_intelligently`` method that can help figure out if the file
needs closing or not.  This is not needed for parameters, but is
necessary for manually prompting with the :func:`prompt` function as you
do not know if a stream like stdout was opened (which was already open
before) or a real file that needs closing.

It is also possible to open files in atomic mode by passing ``atomic=True``.  In atomic mode, all writes go into a separate
file in the same folder, and upon completion, the file will be moved over to
the original location.  This is useful if a file regularly read by other
users is modified.

``Environment Variables``
-------------------------

Like apps, args can also grab values from an environment variable.
Unlike apps, however, this is only supported for explicitly named
environment variables.

Example usage:

.. code:: python

    from quo import echo
    from quo.console import arg, command
    from quo.types import File

    @command()
    @arg('src', envvar='SRC', type=File('r'))
    def echo(src):
        """Print value of SRC environment variable."""
        echo(src.read())


In that case, it can also be a list of different environment variables
where the first one is picked.

Generally, this feature is not recommended because it can cause the user
a lot of confusion.

``App-Like Args``
---------------------

Sometimes, you want to process args that look like apps.  For
instance, imagine you have a file named ``-foo.txt``.  If you pass this as
an arg in this manner, quo will treat it as an app.

To solve this, quo does what any POSIX style command line script does,
and that is to accept the string ``--`` as a separator for options and
arguments.  After the ``--`` marker, all further parameters are accepted as
args.

Example usage:

.. code:: python

    from quo import echo
    from quo.console import arg, command
    from quo.types import Path

    @command()
    @arg('files', nargs=-1, type=Path())
    def touch(files):
        """Print all FILES file names."""
        for filename in files:
            echo(filename)


If you don't like the ``-`` marker, you can set ignore_unknown_apps to
True to avoid checking unknown apps:

.. code:: python

 from quo import echo
 from quo.console import arg, command
 from quo.types import Path

 @command(context_settings={"ignore_unknown_options": True})
 @arg('files', nargs=-1, type=Path())
 def touch(files):
     """Print all FILES file names."""
     for filename in files:
         echo(filename)


