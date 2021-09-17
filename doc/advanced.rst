Advanced Patterns
=================

.. currentmodule:: quo

In addition to common functionality that is implemented in the library
itself, there are countless patterns that can be implemented by extending
Quo.  This page should give some insight into what can be accomplished.

.. _aliases:

Command Aliases
---------------

Many tools support aliases for commands (see `Command alias example
<https://github.com/secretum-inc/quo/tree/main/examples/aliases>`_).
For instance, you can configure ``git`` to accept ``git ci`` as alias for
``git commit``.  Other tools also support auto-discovery for aliases by
automatically shortening them.

Quo does not support this out of the box, but it's very easy to customize
the :class:`Tether` or any other :class:`MultiCommand` to provide this
functionality.

As explained in :ref:`custom-multi-commands`, a multi command can provide
two methods: :meth:`~MultiCommand.list_commands` and
:meth:`~MultiCommand.get_command`.  In this particular case, you only need
to override the latter as you generally don't want to enumerate the
aliases on the help page in order to avoid confusion.

This following example implements a subclass of :class:`Tether` that
accepts a prefix for a command.  If there were a command called ``push``,
it would accept ``pus`` as an alias (so long as it was unique):

.. code-block:: python

   from quo import Tether

    
   class AliasedTether(Tether):

        def get_command(self, clime, cmd_name):
            rv = Tether.get_command(self, clime, cmd_name)
            if rv is not None:
                return rv
            matches = [x for x in self.list_commands(clime)
                       if x.startswith(cmd_name)]
            if not matches:
                return None
            elif len(matches) == 1:
                return Tether.get_command(self, clime, matches[0])
            clime.fail(f"Too many matches: {', '.join(sorted(matches))}")

And it can then be used like this:

.. code-block:: python

    @quo.command(class=AliasedTether)
    def cli():
        pass

    @cli.command()
    def push():
        pass

    @cli.command()
    def pop():
        pass

Parameter Modifications
-----------------------

Parameters (apps and args) are forwarded to the command callbacks
as you have seen.  One common way to prevent a parameter from being passed
to the callback is the `expose_value` argument to a parameter which hides
the parameter entirely.  The way this works is that the :class:`Context`
object has a :attr:`~Context.params` attribute which is a dictionary of
all parameters.  Whatever is in that dictionary is being passed to the
callbacks.

This can be used to make up addition parameters.
.. code-block:: python

    import urllib
    from quo import app command, echo

    class URL(object):

        def __init__(self, url, fp):
            self.url = url
            self.fp = fp

    def open_url(clime, param, value):
        if value is not None:
            return URL(value, urllib.urlopen(value))

    @command()
    @app('--url', callback=open_url)
    def cli(url):
        if url is not None:
            echo(f"{url.url}: {url.fp.code}")


Token Normalization
-------------------

It's possible to provide a function that is used
for normalizing tokens.  Tokens are app names, choice values, or command
values.  This can be used to implement case insensitive apps, for
instance.

In order to use this feature, the context needs to be passed a function that
performs the normalization of the token.  For instance, you could have a
function that converts the token to lowercase:

.. code-block:: python

    import quo
    from quo import command, app, echo
    CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())

    @command(context_settings=CONTEXT_SETTINGS)
    @app('--name', default='Pete')
    def cli(name):
        echo(f"Name: {name}")


.. _callback-evaluation-order:

Callback Evaluation Order
-------------------------

Generally, the order of invocation is driven by the order in which the user
provides the args to the script; if there is an app called ``--foo``
and an app called ``--bar`` and the user calls it as ``--bar
--foo``, then the callback for ``bar`` will fire before the one for ``foo``.

There are three exceptions to this rule which are important to know:

Eagerness:
    An app can be set to be "eager".  All eager parameters are
    evaluated before all non-eager parameters, but again in the order as
    they were provided on the command line by the user.

    This is important for parameters that execute and exit like ``--help``
    and ``--version``.  Both are eager parameters, but whatever parameter
    comes first on the command line will win and exit the program.

Repeated parameters:
    If an app or argument is split up on the command line into multiple
    places because it is repeated -- for instance, ``--exclude foo --include
    baz --exclude bar`` -- the callback will fire based on the position of
    the first app.  In this case, the callback will fire for
    ``exclude`` and it will be passed both apps (``foo`` and
    ``bar``), then the callback for ``include`` will fire with ``baz``
    only.

    Note that even if a parameter does not allow multiple versions, Quo
    will still accept the position of the first, but it will ignore every
    value except the last.  The reason for this is to allow composability
    through shell aliases that set defaults.

Missing parameters:
    If a parameter is not defined on the command line, the callback will
    still fire.
Most of the time you do not need to be concerned about any of this,
but it is important to know how it works for some advanced cases.

.. _forwarding-unknown-apps:

Forwarding Unknown Apps
--------------------------

In some situations it is interesting to be able to accept all unknown
apps for further manual processing.  Quo can generally do that but it has some limitations that lie in the nature of the
problem.  The support for this is provided through a parser flag called
``ignore_unknown_apps`` which will instruct the parser to collect all
unknown apps and to put them to the leftover argument instead of
triggering a parsing error.

It can be enabled by changing the attribute of the same name on the
    context class (:attr:`Context.ignore_unknown_apps`).  This is best
    changed through the ``context_settings`` dictionary on the command.

For most situations the easiest solution is the second.  Once the behavior
is changed something needs to pick up those leftover apps (which at
this point are considered arguments).  For this again you have two
options:

1.  You can use :func:`pass_context` to get the context passed.  This will
    only work if in addition to :attr:`~Context.ignore_unknown_apps`
    you also set :attr:`~Context.allow_extra_args` as otherwise the
    command will abort with an error that there are leftover arguments.
    If you go with this solution, the extra arguments will be collected in
    :attr:`Context.args`.
2.  You can attach a :func:`arg` with ``nargs`` set to `-1` which
    will eat up all leftover arguments.  In this case it's recommended to
    set the `type` to :data:`UNPROCESSED` to avoid any string processing
    on those arguments as otherwise they are forced into unicode strings
    automatically which is often not what you want.

In the end you end up with something like this:

.. code-block:: python

    import sys
    from subprocess import call

    @quo.command(context_settings=dict(
        ignore_unknown_apps=True,
    ))
    @quo.app('-v', '--verbose', is_flag=True, help='Enables verbose mode')
    @quo.arg('timeit_args', nargs=-1, type=quo.UNPROCESSED
    def cli(verbose, timeit_args):
        """A fake wrapper around Python's timeit."""
        cmdline = ['echo', 'python', '-mtimeit'] + list(timeit_args)
        if verbose:
            quo.echo(f"Invoking: {' '.join(cmdline)}")
        call(cmdline)


As you can see the verbosity flag is handled by Quo, everything else
ends up in the `timeit_args` variable for further processing which then
for instance, allows invoking a subprocess.  There are a few things that
are important to know about how this ignoring of unhandled flag happens:

*   Unknown long apps are generally ignored and not processed at all.
    So for instance if ``--foo=bar`` or ``--foo bar`` are passed they
    generally end up like that.  Note that because the parser cannot know
    if an app will accept an argument or not, the ``bar`` part might be
    handled as an argument.
*   Unknown short apps might be partially handled and reassembled if
    necessary.  For instance in the above example there is an app
    called ``-v`` which enables verbose mode.  If the command would be
    ignored with ``-va`` then the ``-v`` part would be handled by Quo
    (as it is known) and ``-a`` would end up in the leftover parameters
    for further processing.
*   Depending on what you plan on doing you might have some success by
    disabling interspersed arguments
    (:attr:`~Context.allow_interspersed_args`) which instructs the parser
    to not allow args and apps to be mixed.  Depending on your
    situation this might improve your results.

Generally though the combinated handling of apps and arguments from
your own commands and commands from another application are discouraged
and if you can avoid it, you should.  It's a much better idea to have
everything below a subcommand be forwarded to another application than to
handle some arguments yourself.


Global Context Access
---------------------

It is possible to access the current context from
anywhere within the same thread through the use of the
:func:`currentcontext` function which returns it.  This is primarily
useful for accessing the context bound object as well as some flags that
are stored on it to customize the runtime behavior.  For instance the
:func:`echo` function does this to infer the default value of the `color`
flag.

Example usage:

.. code:: python

   from quo import currentcontext
    def get_current_command_name():
        return currentcontext().info_name

It should be noted that this only works within the current thread.  If you
spawn additional threads then those threads will not have the ability to
refer to the current context.  If you want to give another thread the
ability to refer to this context you need to use the context within the
thread as a context manager:

.. code:: python

    def spawn_thread(clime, func):
        def wrapper():
            with clime:
                func()
        t = threading.Thread(target=wrapper)
        t.start()
        return t

Now the thread function can access the context like the main thread would
do.  However if you do use this for threading you need to be very careful
as the vast majority of the context is not thread safe!  You are only
allowed to read from the context, but not to perform any modifications on
it.


Detecting the Source of a Parameter
-----------------------------------

In some situations it's helpful to understand whether or not an app
or parameter came from the command line, the environment, the default
<F11>value, or :attr:`Context.default_map`. The
:meth:`Context.get_parameter_source` method can be used to find this
out. It will return a member of the :class:`~quo.core.ParameterSource`
enum.

.. code:: python

    import quo
    from quo import command, arg, echo
    @command()
    @arg('port', nargs=1, default=8080, envvar="PORT")
    @quo.pass_context
    def cli(clime, port):
        source = clime.get_parameter_source("port")
        echo(f"Port came from {source.name}")


Managing Resources
------------------

It can be useful to open a resource in a tether, to be made available to
subcommands. Many types of resources need to be closed or otherwise
cleaned up after use. The standard way to do this in Python is by using
a context manager with the ``with`` statement.

For example, the ``Repo`` class from :doc:`complex` might actually be
defined as a context manager:

.. code-block:: python

    class Repo:
        def __init__(self, home=None):
            self.home = os.path.abspath(home or ".")
            self.db = None

        def __enter__(self):
            path = os.path.join(self.home, "repo.db")
            self.db = open_database(path)

        def __exit__(self, exc_type, exc_value, tb):
            self.db.close()

Ordinarily, it would be used with the ``with`` statement:

.. code-block:: python

    with Repo() as repo:
        repo.db.query(...)

However, a ``with`` block in a tether would exit and close the database
before it could be used by a subcommand.

Instead, use the context's :meth:`~quo.Context.with_resource` method
to enter the context manager and return the resource. When the tether and
any subcommands finish, the context's resources are cleaned up.

.. code-block:: python

    import quo
    from quo import tether, app, echo
    @tether()
    @app("--repo-home", default=".repo")
    @quo.pass_context
    def cli(clime, repo_home):
        clime.obj = clime.with_resource(Repo(repo_home))

    @cli.command()
    @quo.pass_obj
    def log(obj):
        # obj is the repo opened in the cli tether
        for entry in obj.db.query(...):
            echo(entry)

If the resource isn't a context manager, usually it can be wrapped in
one using something from :mod:`contextlib`. If that's not possible, use
the context's :meth:`~quo.Context.call_on_close` method to register a
cleanup function.

.. code-block:: python

    import quo
    from quo import tether, app
    @tether()
    @app("--name", default="repo.db")
    @quo.pass_context
    def cli(clime, repo_home):
        clime.obj = db = open_db(repo_home)

        @clime.call_on_close
        def close_db():
            db.record_use()
            db.save()
            db.close()
