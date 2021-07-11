.. _apps:

Apps
=======

.. currentmodule:: quo

Options can be added/nested to commands using the :func:`app` decorator.  Since apps can come in various different versions, there
Options in quo are highly configurable and should not be confused with :ref:`positional arguments <arguments>`.

How to name Apps
-----------------

A name is chosen in the following order

1.  In the event that a name is not prefixed, therefore it is used as the Python argument name
2.  If there is at least one name prefixed with two dashes, the first
    one given is used as the name.
3.  The first name prefixed with one dash is used otherwise.

To get the Python argument name, the chosen name is converted to lower
case, up to two dashes are removed as the prefix, and other dashes are
converted to underscores.
NB: Options are given as position arguments to the decorator.

.. code-block:: python

    @quo.command()
    @quo.option('-s', '--string-to-echo')
    def echo(string_to_echo):
        quo.echo(string_to_echo)

.. code-block:: python

    from quo import command, app, echo
    @command()
    @app('-s', '--string-to-echo', 'string')
    def echo(string):
        echo(string)

-   ``"-f", "--foo-bar"``, the name is ``foo_bar``
-   ``"-x"``, the name is ``x``
-   ``"-f", "--filename", "dest"``, the name is  ``dest``
-   ``"--CamelCase"``, the name is ``camelcase``
-   ``"-f", "-fb"``, the name is ``f``
-   ``"--f", "--foo-bar"``, the name is ``f``
-   ``"---f"``, the name is ``_f``

Basic Value Options
-------------------

The most basic option is a value option.  These options accept one
argument which is a value.  If no type is provided, the type of the default
value is used.  If no default value is provided, the type is assumed to be
:data:`STRING`.  Unless a name is explicitly specified, the name of the
parameter is the first long option defined; otherwise the first short one is
used. By default, options are not required, however to make an option required,
simply pass in `required=True` as an argument to the decorator.

.. code-block:: python

    @quo.command()
    @quo.option('--n', default=1)
    def dots(n):
        quo.echo('.' * n)

.. code-block:: python

    # How to make an option required
    @quo.command()
    @quo.option('--n', required=True, type=int)
    def dots(n):
        quo.echo('.' * n)

.. code-block:: python

    # How to use a Python reserved word such as `from` as a parameter
    @quo.command()
    @quo.option('--from', '-f', 'from_')
    @quo.option('--to', '-t')
    def reserved_param_name(from_, to):
        quo.echo(f"from {from_} to {to}")

And on the command line:

.. code-block:: python

   invoke(dots, args=['--n=2'])

In this case the option is of type :data:`INT` because the default value
is an integer.

To show the default values when showing command help, use ``show_default=True``

.. code-block:: python

    @quo.command()
    @quo.option('--n', default=1, show_default=True)
    def dots(n):
        quo.echo('.' * n)

.. quo:run::

   invoke(dots, args=['--help'])

Multi Value Apps
-------------------

Sometimes, you have options that take more than one argument.  For options,
only a fixed number of arguments is supported.  This can be configured by
the ``nargs`` parameter.  The values are then stored as a tuple.

.. code-block:: python

    @quo.command()
    @quo.option('--pos', nargs=2, type=float)
    def findme(pos):
        a, b = pos
        quo.echo(f"{a} / {b}")

And on the command line:

.. quo:run::

    invoke(findme, args=['--pos', '2.0', '3.0'])

.. _tuple-type:

Tuples as Multi Value Apps
-----------------------------


As you can see that by using `nargs` set to a specific number each item in
the resulting tuple is of the same type.  This might not be what you want.
Commonly you might want to use different types for different indexes in
the tuple.  For this you can directly specify a tuple as type:

.. code-block:: python

    @quo.command()
    @quo.option('--item', type=(str, int))
    def putitem(item):
        name, id = item
        quo.echo(f"name={name} id={id}")

And on the command line:

.. quo:run::

    invoke(putitem, args=['--item', 'peter', '1338'])

By using a tuple literal as type, `nargs` gets automatically set to the
length of the tuple and the :class:`quo.Tuple` type is automatically
used.  The above example is thus equivalent to this:

.. code-block:: python

    @quo.command()
    @quo.option('--item', nargs=2, type=quo.Tuple([str, int]))
    def putitem(item):
        name, id = item
        quo.echo(f"name={name} id={id}")

.. _multiple-options:

Multiple Apps
----------------

Similarly to ``nargs``, there is also the case of wanting to support a
parameter being provided multiple times and have all the values recorded --
not just the last one.  For instance, ``git commit -m foo -m bar`` would
record two lines for the commit message: ``foo`` and ``bar``. This can be
accomplished with the ``multiple`` flag:

Example:

.. code-block:: python

    @quo.command()
    @quo.option('--message', '-m', multiple=True)
    def commit(message):
        quo.echo('\n'.join(message))

And on the command line:

.. quo:run::

    invoke(commit, args=['-m', 'foo', '-m', 'bar'])

When passing a ``default`` with ``multiple=True``, the default value
must be a list or tuple, otherwise it will be interpreted as a list of
single characters.

.. code-block:: python

    @quo.option("--format", multiple=True, default=["json"])


Counting
--------

In some very rare circumstances, it is interesting to use the repetition
of options to count an integer up.  This can be used for verbosity flags,
for instance:

.. code-block:: python

    @quo.command()
    @quo.option('-v', '--verbose', count=True)
    def log(verbose):
        quo.echo(f"Verbosity: {verbose}")

And on the command line:

.. quo:run::

    invoke(log, args=['-vvv'])

Boolean Flags
-------------

Boolean flags are options that can be enabled or disabled.  This can be
accomplished by defining two flags in one go separated by a slash (``/``)
for enabling or disabling the option.  (If a slash is in an option string,
quo automatically knows that it's a boolean flag and will pass
``is_flag=True`` implicitly.)  quo always wants you to provide an enable
and disable flag so that you can change the default later.

Example:

.. code-block:: python

    import sys

    @quo.command()
    @quo.option('--shout/--no-shout', default=False)
    def info(shout):
        rv = sys.platform
        if shout:
            rv = rv.upper() + '!!!!111'
        quo.echo(rv)

And on the command line:

.. quo:run::

    invoke(info, args=['--shout'])
    invoke(info, args=['--no-shout'])
    invoke(info)

If you really don't want an off-switch, you can just define one and
manually inform quo that something is a flag:

.. code-block:: python

    import sys

    @quo.command()
    @quo.option('--shout', is_flag=True)
    def info(shout):
        rv = sys.platform
        if shout:
            rv = rv.upper() + '!!!!111'
        quo.echo(rv)

And on the command line:

.. quo:run::

    invoke(info, args=['--shout'])
    invoke(info)

Note that if a slash is contained in your option already (for instance, if
you use Windows-style parameters where ``/`` is the prefix character), you
can alternatively split the parameters through ``;`` instead:

.. code-block:: python

    @quo.command()
    @quo.option('/debug;/no-debug')
    def log(debug):
        quo.echo(f"debug={debug}")

    if __name__ == '__main__':
        log()

.. versionchanged:: 6.0

If you want to define an alias for the second option only, then you will
need to use leading whitespace to disambiguate the format string:

Example:

.. code-block:: python

    import sys

    @quo.command()
    @quo.option('--shout/--no-shout', ' /-S', default=False)
    def info(shout):
        rv = sys.platform
        if shout:
            rv = rv.upper() + '!!!!111'
        quo.echo(rv)

.. quo:run::

    invoke(info, args=['--help'])

Feature Switches
----------------

In addition to boolean flags, there are also feature switches.  These are
implemented by setting multiple options to the same parameter name and
defining a flag value.  Note that by providing the ``flag_value`` parameter,
quo will implicitly set ``is_flag=True``.

To set a default flag, assign a value of `True` to the flag that should be
the default.

.. code-block:: python

    import sys

    @quo.command()
    @quo.option('--upper', 'transformation', flag_value='upper',
                  default=True)
    @quo.option('--lower', 'transformation', flag_value='lower')
    def info(transformation):
        quo.echo(getattr(sys.platform, transformation)())

And on the command line:

.. quo:run::

    invoke(info, args=['--upper'])
    invoke(info, args=['--lower'])
    invoke(info)

.. _choice-opts:

Choice Options
--------------

Sometimes, you want to have a parameter be a choice of a list of values.
In that case you can use :class:`Choice` type.  It can be instantiated
with a list of valid values.  The originally passed choice will be returned,
not the str passed on the command line.  Token normalization functions and
``case_sensitive=False`` can cause the two to be different but still match.

Example:

.. code-block:: python

    @quo.command()
    @quo.option('--hash-type',
                  type=quo.Choice(['MD5', 'SHA1'], case_sensitive=False))
    def digest(hash_type):
        quo.echo(hash_type)

What it looks like:

.. quo:run::

    invoke(digest, args=['--hash-type=MD5'])
    println()
    invoke(digest, args=['--hash-type=md5'])
    println()
    invoke(digest, args=['--hash-type=foo'])
    println()
    invoke(digest, args=['--help'])

Only pass the choices as list or tuple. Other iterables (like
generators) may lead to unexpected results.

Choices work with options that have ``multiple=True``. If a ``default``
value is given with ``multiple=True``, it should be a list or tuple of
valid choices.

Choices should be unique after considering the effects of
``case_sensitive`` and any specified token normalization function.

.. versionchanged:: 7.1
    The resulting value from an option will always be one of the
    originally passed choices regardless of ``case_sensitive``.

.. _option-prompting:

Prompting
---------

In some cases, you want parameters that can be provided from the command line,
but if not provided, ask for user input instead.  This can be implemented with
quo by defining a prompt string.

Example:

.. code-block:: python

    @quo.command()
    @quo.option('--name', prompt=True)
    def hello(name):
        quo.echo(f"Hello {name}!")

And what it looks like:

.. quo:run::

    invoke(hello, args=['--name=John'])
    invoke(hello, input=['John'])

If you are not happy with the default prompt string, you can ask for
a different one:

.. code-block:: python

    @quo.command()
    @quo.option('--name', prompt='Your name please')
    def hello(name):
        quo.echo(f"Hello {name}!")

What it looks like:

.. quo:run::

    invoke(hello, input=['John'])

It is advised that prompt not be used in conjunction with the multiple
flag set to True. Instead, prompt in the function interactively.

By default, the user will be prompted for an input if one was not passed
through the command line. To turn this behavior off, see
:ref:`optional-value`.


Password Prompts
----------------

quo also supports hidden prompts and asking for confirmation.  This is
useful for password input:

.. code-block:: python

    import codecs

    @quo.command()
    @quo.option(
        "--password", prompt=True, hide_input=True,
        confirmation_prompt=True
    )
    def encode(password):
        quo.echo(f"encoded: {codecs.encode(password, 'rot13')}")

.. quo:run::

    invoke(encode, input=['secret', 'secret'])

Because this combination of parameters is quite common, this can also be
replaced with the :func:`autopswd` decorator:

.. code-block:: python

    @quo.command()
    @quo.autopswd()
    def encrypt(password):
        quo.echo(f"encoded: to {codecs.encode(password, 'rot13')}")


Dynamic Defaults for Prompts
----------------------------

The ``auto_envvar_prefix`` and ``default_map`` options for the context
allow the program to read option values from the environment or a
configuration file.  However, this overrides the prompting mechanism, so
that the user does not get the option to change the value interactively.

If you want to let the user configure the default value, but still be
prompted if the app isn't specified on the command line, you can do so
by supplying a callable as the default value. For example, to get a default
from the environment:

.. code-block:: python

    import os

    @quo.command()
    @quo.app(
        "--username", prompt=True,
        default=lambda: os.environ.get("USER", "")
    )
    def hello(username):
        quo.echo(f"Hello, {username}!")

To describe what the default value will be, set it in ``show_default``.

.. code-block:: python

    import os

    @quo.command()
    @quo.app(
        "--username", prompt=True,
        default=lambda: os.environ.get("USER", ""),
        show_default="current user"
    )
    def hello(username):
        quo.echo(f"Hello, {username}!")

.. quo:run::

   invoke(hello, args=["--help"])


Callbacks and Eager Options
---------------------------

Sometimes, you want a parameter to completely change the execution flow.
For instance, this is the case when you want to have a ``--version``
parameter that prints out the version and then exits the application.

Note: an actual implementation of a ``--version`` parameter that is
reusable is available in quo as :func:`quo.version_option`.  The code
here is merely an example of how to implement such a flag.

In such cases, you need two concepts: eager parameters and a callback.  An
eager parameter is a parameter that is handled before others, and a
callback is what executes after the parameter is handled.  The eagerness
is necessary so that an earlier required parameter does not produce an
error message.  For instance, if ``--version`` was not eager and a
parameter ``--foo`` was required and defined before, you would need to
specify it for ``--version`` to work.  For more information, see
:ref:`callback-evaluation-order`.

A callback is a function that is invoked with two parameters: the current
:class:`Context` and the value.  The context provides some useful features
such as quitting the application and gives access to other already
processed parameters.

Here an example for a ``--version`` flag:

.. code-block:: python

    def print_version(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        quo.echo('Version 1.0')
        ctx.exit()

    @quo.command()
    @quo.app('--version', is_flag=True, callback=print_version,
                  expose_value=False, is_eager=True)
    def hello():
        quo.echo('Hello World!')

The `expose_value` parameter prevents the pretty pointless ``version``
parameter from being passed to the callback.  If that was not specified, a
boolean would be passed to the `hello` script.  The `resilient_parsing`
flag is applied to the context if quo wants to parse the command line
without any destructive behavior that would change the execution flow.  In
this case, because we would exit the program, we instead do nothing.

What it looks like:

.. quo:run::

    invoke(hello)
    invoke(hello, args=['--version'])

.. admonition:: Callback Signature Changes

    In quo 2.0 the signature for callbacks changed.  For more
    information about these changes see :ref:`upgrade-to-2.0`.

Yes Parameters
--------------

For dangerous operations, it's very useful to be able to ask a user for
confirmation.  This can be done by adding a boolean ``--yes`` flag and
asking for confirmation if the user did not provide it and to fail in a
callback:

.. code-block:: python

    def abort_if_false(ctx, param, value):
        if not value:
            ctx.abort()

    @quo.command()
    @quo.app('--yes', is_flag=True, callback=abort_if_false,
                  expose_value=False,
                  prompt='Are you sure you want to drop the db?')
    def dropdb():
        quo.echo('Dropped all tables!')

And what it looks like on the command line:

.. quo:run::

    invoke(dropdb, input=['n'])
    invoke(dropdb, args=['--yes'])

Because this combination of parameters is quite common, this can also be
replaced with the :func:`autoconfirm` decorator:

.. code-block:: python

    @quo.command()
    @quo.autoconfirm(prompt='Are you sure you want to drop the db?')
    def dropdb():
        quo.echo('Dropped all tables!')

.. admonition:: Callback Signature Changes

    
Values from Environment Variables
---------------------------------

A very useful feature of quo is the ability to accept parameters from
environment variables in addition to regular parameters.  This allows
tools to be automated much easier.  For instance, you might want to pass
a configuration file with a ``--config`` parameter but also support exporting
a ``TOOL_CONFIG=hello.cfg`` key-value pair for a nicer development
experience.

This is supported by quo in two ways.  One is to automatically build
environment variables which is supported for apps only.  To enable this
feature, the ``auto_envvar_prefix`` parameter needs to be passed to the
script that is invoked.  Each command and parameter is then added as an
uppercase underscore-separated variable.  If you have a subcommand
called ``run`` taking an app called ``reload`` and the prefix is
``WEB``, then the variable is ``WEB_RUN_RELOAD``.

Example usage:

.. code-block:: python

    @quo.command()
    @quo.app('--username')
    def greet(username):
        quo.echo(f'Hello {username}!')

    if __name__ == '__main__':
        greet(auto_envvar_prefix='GREETER')

And from the command line:

.. quo:run::

    invoke(greet, env={'GREETER_USERNAME': 'john'},
           auto_envvar_prefix='GREETER')

When using ``auto_envvar_prefix`` with command groups, the command name
needs to be included in the environment variable, between the prefix and
the parameter name, *i.e.* ``PREFIX_COMMAND_VARIABLE``. If you have a
subcommand called ``run-server`` taking an app called ``host`` and
the prefix is ``WEB``, then the variable is ``WEB_RUN_SERVER_HOST``.

Example:

.. code-block:: python

   @quo.group()
   @quo.app('--debug/--no-debug')
   def cli(debug):
       quo.echo(f"Debug mode is {'on' if debug else 'off'}")

   @cli.command()
   @quo.app('--username')
   def greet(username):
       quo.echo(f"Hello {username}!")

   if __name__ == '__main__':
       cli(auto_envvar_prefix='GREETER')

.. quo:run::

   invoke(cli, args=['greet',],
          env={'GREETER_GREET_USERNAME': 'John', 'GREETER_DEBUG': 'false'},
          auto_envvar_prefix='GREETER')


The second option is to manually pull values in from specific environment
variables by defining the name of the environment variable on the app.

Example usage:

.. code-block:: python

    @quo.command()
    @quo.app('--username', envvar='USERNAME')
    def greet(username):
       quo.echo(f"Hello {username}!")

    if __name__ == '__main__':
        greet()

And from the command line:

.. quo:run::

    invoke(greet, env={'USERNAME': 'john'})

In that case it can also be a list of different environment variables
where the first one is picked.

Multiple Values from Environment Values
---------------------------------------

As apps can accept multiple values, pulling in such values from
environment variables (which are strings) is a bit more complex.  The way
quo solves this is by leaving it up to the type to customize this
behavior.  For both ``multiple`` and ``nargs`` with values other than
``1``, quo will invoke the :meth:`ParamType.split_envvar_value` method to
perform the splitting.

The default implementation for all types is to split on whitespace.  The
exceptions to this rule are the :class:`File` and :class:`Path` types
which both split according to the operating system's path splitting rules.
On Unix systems like Linux and OS X, the splitting happens for those on
every colon (``:``), and for Windows, on every semicolon (``;``).

Example usage:

.. code-block:: python

    @quo.command()
    @quo.app('paths', '--path', envvar='PATHS', multiple=True,
                  type=quo.Path())
    def perform(paths):
        for path in paths:
            quo.echo(path)

    if __name__ == '__main__':
        perform()

And from the command line:

.. quo:run::

    import os
    invoke(perform, env={"PATHS": f"./foo/bar{os.path.pathsep}./test"})

Other Prefix Characters
-----------------------

quo can deal with alternative prefix characters other than ``-`` for
apps.  This is for instance useful if you want to handle slashes as
parameters ``/`` or something similar.  Note that this is strongly
discouraged in general because quo wants developers to stay close to
POSIX semantics.  However in certain situations this can be useful:

.. code-block:: python

    @quo.command()
    @quo.app('+w/-w')
    def chmod(w):
        quo.echo(f"writable={w}")

    if __name__ == '__main__':
        chmod()

And from the command line:

.. quo:run::

    invoke(chmod, args=['+w'])
    invoke(chmod, args=['-w'])

Note that if you are using ``/`` as prefix character and you want to use a
boolean flag you need to separate it with ``;`` instead of ``/``:

.. code-block:: python

    @quo.command()
    @quo.app('/debug;/no-debug')
    def log(debug):
        quo.echo(f"debug={debug}")

    if __name__ == '__main__':
        log()

.. _ranges:

Range Options
-------------

The :class:`IntRange` type extends the :data:`INT` type to ensure the
value is contained in the given range. The :class:`FloatRange` type does
the same for :data:`FLOAT`.

If ``min`` or ``max`` is omitted, that side is *unbounded*. Any value in
that direction is accepted. By default, both bounds are *closed*, which
means the boundary value is included in the accepted range. ``min_open``
and ``max_open`` can be used to exclude that boundary from the range.

If ``clamp`` mode is enabled, a value that is outside the range is set
to the boundary instead of failing. For example, the range ``0, 5``
would return ``5`` for the value ``10``, or ``0`` for the value ``-1``.
When using :class:`FloatRange`, ``clamp`` can only be enabled if both
bounds are *closed* (the default).

.. code-block:: python

    @quo.command()
    @quo.app("--count", type=quo.IntRange(0, 20, clamp=True))
    @quo.app("--digit", type=quo.IntRange(0, 9))
    def repeat(count, digit):
        quo.echo(str(digit) * count)

.. quo:run::

    invoke(repeat, args=['--count=100', '--digit=5'])
    invoke(repeat, args=['--count=6', '--digit=12'])


Callbacks for Validation
------------------------

If you want to apply custom validation logic, you can do this in the
parameter callbacks. These callbacks can both modify values as well as
raise errors if the validation does not work. The callback runs after
type conversion. It is called for all sources, including prompts.

.. code-block:: python

    def validate_rolls(ctx, param, value):
        if isinstance(value, tuple):
            return value

        try:
            rolls, _, dice = value.partition("d")
            return int(dice), int(rolls)
        except ValueError:
            raise quo.BadParameter("format must be 'NdM'")

    @quo.command()
    @quo.app(
        "--rolls", type=quo.UNPROCESSED, callback=validate_rolls,
        default="1d6", prompt=True,
    )
    def roll(rolls):
        sides, times = rolls
        quo.echo(f"Rolling a {sides}-sided dice {times} time(s)")

.. quo:run::

    invoke(roll, args=["--rolls=42"])
    println()
    invoke(roll, args=["--rolls=2d12"])
    println()
    invoke(roll, input=["42", "2d12"])


.. _optional-value:

Optional Value
--------------

Providing the value to an app can be made optional, in which case
providing only the app's flag without a value will either show a
prompt or use its ``flag_value``.

Setting ``is_flag=False, flag_value=value`` tells quo that the app
can still be passed a value, but if only the flag is given the
``flag_value`` is used.

.. code-block:: python

    @quo.command()
    @quo.app("--name", is_flag=False, flag_value="Flag", default="Default")
    def hello(name):
        quo.echo(f"Hello, {name}!")

.. code-block:: python

    invoke(hello, args=[])
    invoke(hello, args=["--name", "Value"])
    invoke(hello, args=["--name"])

If the app has ``prompt`` enabled, then setting
``prompt_required=False`` tells quo to only show the prompt if the
app's flag is given, instead of if the app is not provided at all.

.. code-block:: python

    @quo.command()
    @quo.app('--name', prompt=True, prompt_required=False, default="Default")
    def hello(name):
        quo.echo(f"Hello {name}!")

.. quo:run::

    invoke(hello)
    invoke(hello, args=["--name", "Value"])
    invoke(hello, args=["--name"], input="Prompt")

If ``required=True``, then the option will still prompt if it is not
given, but it will also prompt if only the flag is given.
