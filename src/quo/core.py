import enum
import errno
import os
import sys
from contextlib import contextmanager, ExitStack
from functools import update_wrapper
from itertools import repeat

from .universal import python_environment
from quo.outliers import (
                   Abort,
                   BadParameter,
                   Exit,
                   MissingParameter,
                   UsageError,
                   QuoException
                   )

from .setout import HelpFormatter
from .setout import join_apps
from quo.context.current import pop_context
from quo.context.current import push_context
from .parser import _flag_needs_value
from .parser import AppParser
from .parser import split_opt
from quo.i_o import (
           confirm,
           echo,
           prompt,
           style
           )

from .types import (
        _NumberRangeBase,
        BOOL,
        convert_type,
        IntRange
        )

from quo.expediency import (
        _detect_program_name,
        inscribe,
        make_default_short_help,
        make_str,
        PacifyFlushWrapper
        )

_missing = object()

SUBCOMMAND_METAVAR = "COMMAND [ARGS]..."
SUBCOMMANDS_METAVAR = "COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]..."

DEPRECATED_HELP_NOTICE = " (DEPRECATED)"
DEPRECATED_INVOKE_NOTICE = "Warning: The command {name} has been deprecated."


def deprecated_notice(cmd):
    if cmd.deprecated:
        echo(DEPRECATED_INVOKE_NOTICE.format(name=cmd.name), fg="black", bg="yellow", err=True)


def quick_exit(code):
    """Low-level exit that skips Python's cleanup but speeds up exit by
    about 10ms for things like shell completion.

    :param code: Exit code.
    """
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)

SHELL_NAMES = (
    {"sh", "bash", "dash", "ash"}  # Bourne.
    | {"csh", "tcsh"}  # C.
    | {"ksh", "zsh", "fish"}  # Common alternatives.
    | {"cmd", "powershell", "pwsh"}  # Microsoft.
    | {"elvish", "xonsh"}  # More exotic.
)


class ShellDetectionFailure(EnvironmentError):
    pass



def _complete_visible_commands(clime, incomplete):
    """List all the subcommands tethered that start with the
    incomplete value and aren't hidden.

    :param clime: Invocation context for the tethered sub-commands.
    :param incomplete: Value being completed. May be empty.
    """
    for name in clime.command.list_commands(clime):
        if name.startswith(incomplete):
            command = clime.command.get_command(clime, name)

            if not command.hidden:
                yield name, command


def multicommand_checker(base_command, cmd_name, cmd, register=False):
    if not base_command.chain or not isinstance(cmd, MultiCommand):
        return
    if register:
        hint = (
            "It is not possible to add multi commands as children to"
            " another multi command that is in chain mode."
        )
    else:
        hint = (
            "Found a multi command as subcommand to a multi command"
            " that is in chain mode. This is not supported."
        )
    raise RuntimeError(
        f"{hint}. Command {base_command.name!r} is set to chain and"
        f" {cmd_name!r} was added as a subcommand but it in itself is a"
        f" multi command. ({cmd_name!r} is a {type(cmd).__name__}"
        f" within a chained {type(base_command).__name__} named"
        f" {base_command.name!r})."
    )


def batch(iterable, batch_size):
    return list(zip(*repeat(iter(iterable), batch_size)))


@contextmanager
def augment_usage_errors(clime, param=None):
    """Context manager that attaches extra information to exceptions."""
    try:
        yield
    except BadParameter as e:
        if e.clime is None:
            e.clime = clime
        if param is not None and e.param is None:
            e.param = param
        raise
    except UsageError as e:
        if e.clime is None:
            e.clime = clime
        raise


def iter_params_for_processing(invocation_order, declaration_order):
    """Given a sequence of parameters in the order as should be considered
    for processing and an iterable of parameters that exist, this returns
    a list in the correct order as they should be processed.
    """

    def sort_key(item):
        try:
            idx = invocation_order.index(item)
        except ValueError:
            idx = float("inf")
        return (not item.is_eager, idx)

    return sorted(declaration_order, key=sort_key)


class ParameterSource(enum.Enum):
    """This is an :class:`~enum.Enum` that indicates the source of a parameter's value.

    Use :meth:`quo.Context.get_parameter_source` to get the source for a parameter by name.

    """

    COMMANDLINE = enum.auto()
    """The value was provided by the command line args."""
    ENVIRONMENT = enum.auto()
    """The value was provided with an environment variable."""
    DEFAULT = enum.auto()
    """Used the default specified by the parameter."""
    DEFAULT_MAP = enum.auto()
    """Used a default provided by :attr:`Context.default_map`."""
    PROMPT = enum.auto()
    """Used a prompt to confirm a default or provide a value."""


class Context:
    """The context is a special internal object that holds state relevant
    for the script execution at every single level.  It's normally invisible
    to commands unless they opt-in to getting access to it.

    The context is useful as it can pass internal objects around and can
    control special execution features such as reading data from
    environment variables.

    A context can be used as context manager in which case it will call
    :meth:`close` on teardown.

    :param command: the command class for this context.
    :param parent: the parent context.
    :param info_name: the info name for this invocation.  Generally this
                      is the most descriptive name for the script or
                      command.  For the toplevel script it is usually
                      the name of the script, for commands below it it's
                      the name of the script.
    :param obj: an arbitrary object of user data.
    :param auto_envvar_prefix: the prefix to use for automatic environment
                               variables.  If this is `None` then reading
                               from environment variables is disabled.  This
                               does not affect manually set environment
                               variables which are always read.
    :param default_map: a dictionary (like object) with default values
                        for parameters.
    :param terminal_width: the width of the terminal.  The default is
                           inherit from parent context.  If no context
                           defines the terminal width then auto
                           detection will be applied.
    :param max_content_width: the maximum width for content rendered by
                              Quo (this currently only affects help
                              pages).  This defaults to 80 characters if
                              not overridden.  In other words: even if the
                              terminal is larger than that, Quo will not
                              format things wider than 80 characters by
                              default.  In addition to that, formatters might
                              add some safety mapping on the right.
    :param resilient_parsing: if this flag is enabled then Quo will
                              parse without any interactivity or callback
                              invocation.  Default values will also be
                              ignored.  This is useful for implementing
                              things such as completion support.
    :param allow_extra_args: if this is set to `True` then extra arguments
                             at the end will not raise an error and will be
                             kept on the context.  The default is to inherit
                             from the command.
    :param allow_interspersed_args: if this is set to `False` then apps
                                    and arguments cannot be mixed.  The
                                    default is to inherit from the command.
    :param ignore_unknown_apps: instructs Quo to ignore apps it does
                                   not know and keeps them for later
                                   processing.
    :param autohelp_names: optionally a list of strings that define how
                              the default help parameter is named.  The
                              default is ``['--help']``.
    :param token_normalize_func: an optional function that is used to
                                 normalize tokens (apps, choices,
                                 etc.).  This for instance can be used to
                                 implement case insensitive behavior.
    :param color: controls if the terminal supports ANSI colors or not.  The
                  default is autodetection.  This is only needed if ANSI
                  codes are used in texts that Quo prints which is by
                  default not the case.  This for instance would affect
                  help output.
    :param show_default: Show defaults for all apps. If not set,
        defaults to the value from a parent context. Overrides an
        app's ``show_default`` argument.

    """

    #: The formatter class to create with :meth:`make_formatter`.
    #:
    #:
    formatter_class = HelpFormatter

    def __init__(
        self,
        command,
        parent=None,
        info_name=None,
        obj=None,
        auto_envvar_prefix=None,
        default_map=None,
        terminal_width=None,
        max_content_width=None,
        resilient_parsing=False,
        allow_extra_args=None,
        allow_interspersed_args=None,
        ignore_unknown_apps=None,
        autohelp_names=None,
        token_normalize_func=None,
        color=None,
        show_default=None,
    ):
        #: the parent context or `None` if none exists.
        self.parent = parent
        #: the :class:`Command` for this context.
        self.command = command
        #: the descriptive information name
        self.info_name = info_name
        #: Map of parameter names to their parsed values. Parameters
        #: with ``expose_value=False`` are not stored.
        self.params = {}
        #: the leftover arguments.
        self.args = []
        #: protected arguments.  These are arguments that are prepended
        #: to `args` when certain parsing scenarios are encountered but
        #: must be never propagated to another arguments.  This is used
        #: to implement nested parsing.
        self.protected_args = []
        if obj is None and parent is not None:
            obj = parent.obj
        #: the user object stored.
        self.obj = obj
        self._meta = getattr(parent, "meta", {})

        #: A dictionary (-like object) with defaults for parameters.
        if (
            default_map is None
            and parent is not None
            and parent.default_map is not None
        ):
            default_map = parent.default_map.get(info_name)
        self.default_map = default_map

        #: This flag indicates if a subcommand is going to be executed. A
        #: tether callback can use this information to figure out if it's
        #: being executed directly or because the execution flow passes
        #: onwards to a subcommand. By default it's None, but it can be
        #: the name of the subcommand to execute.
        #:
        #: If chaining is enabled this will be set to ``'*'`` in case
        #: any commands are executed.  It is however not possible to
        #: figure out which ones.  If you require this knowledge you
        #: should use a :func:`resultcallback`.
        self.invoked_subcommand = None

        if terminal_width is None and parent is not None:
            terminal_width = parent.terminal_width
        #: The width of the terminal (None is autodetection).
        self.terminal_width = terminal_width

        if max_content_width is None and parent is not None:
            max_content_width = parent.max_content_width
        #: The maximum width of formatted content (None implies a sensible
        #: default which is 80 for most things).
        self.max_content_width = max_content_width

        if allow_extra_args is None:
            allow_extra_args = command.allow_extra_args
        #: Indicates if the context allows extra args or if it should
        #: fail on parsing.
        #:
        #:
        self.allow_extra_args = allow_extra_args

        if allow_interspersed_args is None:
            allow_interspersed_args = command.allow_interspersed_args
        #: Indicates if the context allows mixing of arguments and
        #: apps or not.
        #:
        self.allow_interspersed_args = allow_interspersed_args

        if ignore_unknown_apps is None:
            ignore_unknown_apps = command.ignore_unknown_apps
        #: Instructs Quo to ignore apps that a command does not
        #: understand and will store it on the context for later
        #: processing.  This is primarily useful for situations where you
        #: want to call into external programs.  Generally this pattern is
        #: strongly discouraged because it's not possibly to losslessly
        #: forward all arguments.
        #:
        #:
        self.ignore_unknown_apps = ignore_unknown_apps

        if autohelp_names is None:
            if parent is not None:
                autohelp_names = parent.autohelp_names
            else:
                autohelp_names = ["--help"]

        #: The names for the help apps.
        self.autohelp_names = autohelp_names

        if token_normalize_func is None and parent is not None:
            token_normalize_func = parent.token_normalize_func

        #: An optional normalization function for tokens.  This is
        #: apps, choices, commands etc.
        self.token_normalize_func = token_normalize_func

        #: Indicates if resilient parsing is enabled.  In that case Quo
        #: will do its best to not cause any failures and default values
        #: will be ignored. Useful for completion.
        self.resilient_parsing = resilient_parsing

        # If there is no envvar prefix yet, but the parent has one and
        # the command on this level has a name, we can expand the envvar
        # prefix automatically.
        if auto_envvar_prefix is None:
            if (
                parent is not None
                and parent.auto_envvar_prefix is not None
                and self.info_name is not None
            ):
                auto_envvar_prefix = (
                    f"{parent.auto_envvar_prefix}_{self.info_name.upper()}"
                )
        else:
            auto_envvar_prefix = auto_envvar_prefix.upper()
        if auto_envvar_prefix is not None:
            auto_envvar_prefix = auto_envvar_prefix.replace("-", "_")
        self.auto_envvar_prefix = auto_envvar_prefix

        if color is None and parent is not None:
            color = parent.color

        #: Controls if styling output is wanted or not.
        self.color = color

        if show_default is None and parent is not None:
            show_default = parent.show_default

        #: Show app default values when formatting help text.
        self.show_default = show_default

        self._close_callbacks = []
        self._depth = 0
        self._parameter_source = {}
        self._exit_stack = ExitStack()

    def to_info_dict(self):
        """Gather information that could be useful for a tool generating
        user-facing documentation. This traverses the entire CLI
        structure.

        .. code-block:: python

            with Context(cli) as clime:
                info = clime.to_info_dict()

  
        """
        return {
            "command": self.command.to_info_dict(self),
            "info_name": self.info_name,
            "allow_extra_args": self.allow_extra_args,
            "allow_interspersed_args": self.allow_interspersed_args,
            "ignore_unknown_apps": self.ignore_unknown_apps,
            "auto_envvar_prefix": self.auto_envvar_prefix,
        }

    def __enter__(self):
        self._depth += 1
        push_context(self)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self._depth -= 1
        if self._depth == 0:
            self.close()
        pop_context()

    @contextmanager
    def scope(self, cleanup=True):
        """This helper method can be used with the context object to promote it to the current thread local (see :func:`currentcontext`).
        The default behavior of this is to invoke the cleanup functions which can be disabled by setting `cleanup` to `False`.  The cleanup  functions are typically used for things such as closing file handles.

        If the cleanup is intended the context object can also be directly used as a context manager.

        Example usage::

            with clime.scope():
                assert currentcontext() is clime

        This is equivalent::

            with clime:
                assert currentcontext() is clime


        :param cleanup: controls if the cleanup functions should be run or not.  The default is to run these functions.  In some situations the context only wants to be temporarily pushed in which case this can be disabled. Nested pushes automatically defer the cleanup.
        """
        if not cleanup:
            self._depth += 1
        try:
            with self as rv:
                yield rv
        finally:
            if not cleanup:
                self._depth -= 1

    @property
    def meta(self):
        """This is a dictionary which is shared with all the contexts that are nested.  It exists so that Quo utilities can store some state here if they need to.  It is however the responsibility of that code to manage this dictionary well.
   
   The keys are supposed to be unique dotted strings.  For instance module paths are a good choice for it.  What is stored in there is  irrelevant for the operation of Quo.  However what is important is that code that places data here adheres to the general semantics ofthe system.

        Example usage::

            LANG_KEY = f'{__name__}.lang'

            def set_language(value):
                clime = currentcontext()
                clime.meta[LANG_KEY] = value

            def get_language():
                return currentcontext().meta.get(LANG_KEY, 'en_US')

        """
        return self._meta

    def make_formatter(self):
        """Creates the :class:`~quo.HelpFormatter` for the help and usage output.

        To quickly customize the formatter class used without overriding this method, set the :attr:`formatter_class` attribute.

        """
        return self.formatter_class(
            width=self.terminal_width, max_width=self.max_content_width
        )

    def with_resource(self, context_manager):
        """Register a resource as if it were used in a ``with``
        statement. The resource will be cleaned up when the context is
        popped.

        Uses :meth:`contextlib.ExitStack.enter_context`. It calls the
        resource's ``__enter__()`` method and returns the result. When
        the context is popped, it closes the stack, which calls the
        resource's ``__exit__()`` method.

        To register a cleanup function for something that isn't a
        context manager, use :meth:`call_on_close`. Or use something
        from :mod:`contextlib` to turn it into a context manager first.

        .. code-block:: python

            @quo.tether()
            @quo.app("--name")
            @quo.contextualize
            def cli(clime):
                clime.obj = clime.with_resource(connect_db(name))

        :param context_manager: The context manager to enter.
        :return: Whatever ``context_manager.__enter__()`` returns.

        """
        return self._exit_stack.enter_context(context_manager)

    def call_on_close(self, f):
        """Register a function to be called when the context tears down.

        This can be used to close resources opened during the script
        execution. Resources that support Python's context manager
        protocol which would be used in a ``with`` statement should be
        registered with :meth:`with_resource` instead.

        :param f: The function to execute on teardown.
        """
        return self._exit_stack.callback(f)

    def close(self):
        """Invoke all close callbacks registered with
        :meth:`call_on_close`, and exit all context managers entered
        with :meth:`with_resource`.
        """
        self._exit_stack.close()
        # In case the context is reused, create a new exit stack.
        self._exit_stack = ExitStack()

    @property
    def command_path(self):
        """The computed command path.  This is used for the ``usage``
        information on the help page.  It's automatically created by
        combining the info names of the chain of contexts to the root.
        """
        rv = ""
        if self.info_name is not None:
            rv = self.info_name
        if self.parent is not None:
            parent_command_path = [self.parent.command_path]
            for param in self.parent.command.get_params(self):
                parent_command_path.extend(param.get_usage_pieces(self))
            rv = f"{' '.join(parent_command_path)} {rv}"
        return rv.lstrip()

    def find_root(self):
        """Finds the outermost context."""
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def find_object(self, object_type):
        """Finds the closest object of a given type."""
        node = self
        while node is not None:
            if isinstance(node.obj, object_type):
                return node.obj
            node = node.parent

    def ensure_object(self, object_type):
        """Like :meth:`find_object` but sets the innermost object to a
        new instance of `object_type` if it does not exist.
        """
        rv = self.find_object(object_type)
        if rv is None:
            self.obj = rv = object_type()
        return rv

    def lookup_default(self, name, call=True):
        """Get the default for a parameter from :attr:`default_map`.

        :param name: Name of the parameter.
        :param call: If the default is a callable, call it. Disable to
            return the callable instead.

        """
        if self.default_map is not None:
            value = self.default_map.get(name)

            if call and callable(value):
                return value()

            return value

    def fail(self, message):
        """Aborts the execution of the program with a specific error
        message.

        :param message: the error message to fail with.
        """
        raise UsageError(message, self)

    def abort(self):
        """Aborts the script."""
        raise Abort()

    def exit(self, code=0):
        """Exits the application with a given exit code."""
        raise Exit(code)

    def get_usage(self):
        """Helper method to get formatted usage string for the current context and command.
        """
        return self.command.get_usage(self)

    def get_help(self):
        """Helper method to get formatted help page for the current context and command.
        """
        return self.command.get_help(self)

    def _make_sub_context(self, command):
        """Create a new context of the same type as this context, but for a new command.

        :meta private:
        """
        return type(self)(command, info_name=command.name, parent=self)

    def invoke(*args, **kwargs):  # noqa: B902
        """Invokes a command callback in exactly the way it expects.  There
        are two ways to invoke this method:

        1.  the first argument can be a callback and all other arguments and
            keyword arguments are forwarded directly to the function.
        2.  the first argument is a quo command object.  In that case all
            arguments are forwarded as well but proper quo parameters
            (apps and quo arguments) must be keyword arguments and quo
            will fill in defaults.

        Note that before quo 3.2 keyword arguments were not properly filled
        in against the intention of this code and no context was created.  For
        more information about this change and why it was done in a bugfix
        release see :ref:`upgrade-to-3.2`.
        """
        self, callback = args[:2]
        clime = self

        # It's also possible to invoke another command which might or
        # might not have a callback.  In that case we also fill
        # in defaults and make a new context for this command.
        if isinstance(callback, Command):
            other_cmd = callback
            callback = other_cmd.callback

            if callback is None:
                raise TypeError(
                    "The given command does not have a callback that can be invoked."
                )

            clime = self._make_sub_context(other_cmd)

            for param in other_cmd.params:
                if param.name not in kwargs and param.expose_value:
                    kwargs[param.name] = param.get_default(clime)

        args = args[2:]
        with augment_usage_errors(self):
            with clime:
                return callback(*args, **kwargs)

    def forward(*args, **kwargs):  # noqa: B902
        """Similar to :meth:`invoke` but fills in default keyword
        arguments from the current context if the other command expects
        it.  This cannot invoke callbacks directly, only other commands.
        """
        self, cmd = args[:2]

        # Can only forward to other commands, not direct callbacks.
        if not isinstance(cmd, Command):
            raise TypeError("Callback is not a command.")

        for param in self.params:
            if param not in kwargs:
                kwargs[param] = self.params[param]

        return self.invoke(cmd, **kwargs)

    def set_parameter_source(self, name, source):
        """Set the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.

        :param name: The name of the parameter.
        :param source: A member of :class:`~quo.core.ParameterSource`.
        """
        self._parameter_source[name] = source

    def get_parameter_source(self, name):
        """Get the source of a parameter. This indicates the location
        from which the value of the parameter was obtained.

        This can be useful for determining when a user specified a value
        on the command line that is the same as the default value. It
        will be :attr:`~quo.core.ParameterSource.DEFAULT` only if the
        value was actually taken from the default.

        :param name: The name of the parameter.
        :rtype: ParameterSource

        """
        return self._parameter_source.get(name)


class BaseCommand:
    """The base command implements the minimal API contract of commands.
    Most code will never use this as it does not implement a lot of useful
    functionality but it can act as the direct subclass of alternative
    parsing methods that do not depend on the quo parser.

    For instance, this can be used to bridge quo and other systems like
    argparse or docopt.

    Because base commands do not implement a lot of the API that other
    parts of quo take for granted, they are not supported for all
    operations.  For instance, they cannot be used with the decorators
    usually and they have no built-in callback system.

    :param name: the name of the command to use unless a tether overrides it.
    :param context_settings: an optional dictionary with defaults that are
                             passed to the context object.
    """

    #: The context class to create with :meth:`make_context`.
    #:
    #:
    context_class = Context
    #: the default for the :attr:`Context.allow_extra_args` flag.
    allow_extra_args = False
    #: the default for the :attr:`Context.allow_interspersed_args` flag.
    allow_interspersed_args = True
    #: the default for the :attr:`Context.ignore_unknown_apps` flag.
    ignore_unknown_apps = False

    def __init__(self, name, context_settings=None):
        #: the name the command thinks it has.  Upon registering a command
        #: on a :class:`Tether` the tethered sub-commands will default the command name
        #: with this information.  You should instead use the
        #: :class:`Context`\'s :attr:`~Context.info_name` attribute.
        self.name = name
        if context_settings is None:
            context_settings = {}
        #: an optional dictionary with defaults passed to the context.
        self.context_settings = context_settings

    def to_info_dict(self, clime):
        """Gather information that could be useful for a tool generating
        user-facing documentation. This traverses the entire structure
        below this command.

        Use :meth:`quo.Context.to_info_dict` to traverse the entire
        CLI structure.

        :param clime: A :class:`Context` representing this command.

        """
        return {"name": self.name}

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def get_usage(self, clime):
        raise NotImplementedError("Base commands cannot get usage")

    def get_help(self, clime):
        raise NotImplementedError("Base commands cannot get help")

    def make_context(self, info_name, args, parent=None, **extra):
        """This function when given an info name and arguments will kick
        off the parsing and create a new :class:`Context`.  It does not
        invoke the actual command callback though.

        To quickly customize the context class used without overriding
        this method, set the :attr:`context_class` attribute.

        :param info_name: the info name for this invokation.  Generally this
                          is the most descriptive name for the script or
                          command.  For the toplevel script it's usually
                          the name of the script, for commands below it it's
                          the name of the script.
        :param args: the arguments to parse as list of strings.
        :param parent: the parent context if available.
        :param extra: extra keyword arguments forwarded to the context
                      constructor.

        """
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value

        clime = self.context_class(self, info_name=info_name, parent=parent, **extra)

        with clime.scope(cleanup=False):
            self.parse_args(clime, args)
        return clime

    def parse_args(self, clime, args):
        """Given a context and a list of arguments this creates the parser
        and parses the arguments, then modifies the context as necessary.
        This is automatically invoked by :meth:`make_context`.
        """
        raise NotImplementedError("Base commands do not know how to parse arguments.")

    def invoke(self, clime):
        """Given a context, this invokes the command.  The default
        implementation is raising a not implemented error.
        """
        raise NotImplementedError("Base commands are not invokable by default")

    def shell_complete(self, clime, incomplete):
        """Return a list of completions for the incomplete value. Looks
        at the names of chained multi-commands.

        Any command could be part of a chained multi-command, so sibling
        commands are valid at any point during command completion. Other
        command classes will return more completions.

        :param clime: Invocation context for this command.
        :param incomplete: Value being completed. May be empty.

        """
        from quo.shelldone import CompletionItem

        results = []

        while clime.parent is not None:
            clime = clime.parent

            if isinstance(clime.command, MultiCommand) and clime.command.chain:
                results.extend(
                    CompletionItem(name, help=command.get_short_help_str())
                    for name, command in _complete_visible_commands(clime, incomplete)
                    if name not in clime.protected_args
                )

        return results

    def main(
        self,
        args=None,
        prog_name=None,
        complete_var=None,
        standalone_mode=True,
        **extra,
    ):
        """This is the way to invoke a script with all the bells and
        whistles as a command line application.  This will always terminate
        the application after a call.  If this is not wanted, ``SystemExit``
        needs to be caught.

        This method is also available by directly calling the instance of
        a :class:`Command`.

        :param args: the arguments that should be used for parsing.  If not
                     provided, ``sys.argv[1:]`` is used.
        :param prog_name: the program name that should be used.  By default
                          the program name is constructed by taking the file
                          name from ``sys.argv[0]``.
        :param complete_var: the environment variable that controls the
                             bash completion support.  The default is
                             ``"_<prog_name>_COMPLETE"`` with prog_name in
                             uppercase.
        :param standalone_mode: the default behavior is to invoke the script
                                in standalone mode.  quo will then
                                handle exceptions and convert them into
                                error messages and the function will never
                                return but shut down the interpreter.  If
                                this is set to `False` they will be
                                propagated to the caller and the return
                                value of this function is the return value
                                of :meth:`invoke`.
        :param extra: extra keyword arguments are forwarded to the context
                      constructor.  See :class:`Context` for more information.
        """
        # Verify that the environment is configured correctly, or reject
        # further execution to avoid a broken script.
        python_environment()

        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)

        if prog_name is None:
            prog_name = _detect_program_name()

        # Process shell completion requests and exit early.
        self._main_shelldone(extra, prog_name, complete_var)

        try:
            try:
                with self.make_context(prog_name, args, **extra) as clime:
                    rv = self.invoke(clime)
                    if not standalone_mode:
                        return rv
                    # it's not safe to `clime.exit(rv)` here!
                    # note that `rv` may actually contain data like "1" which
                    # has obvious effects
                    # more subtle case: `rv=[None, None]` can come out of
                    # chained commands which all returned `None` -- so it's not
                    # even always obvious that `rv` indicates success/failure
                    # by its truthiness/falsiness
                    clime.exit()
            except (EOFError, KeyboardInterrupt):
                echo(file=sys.stderr,fg="red")
                raise Abort()
            except QuoException as e:
                if not standalone_mode:
                    raise
                e.show()
                sys.exit(e.exit_code)
            except OSError as e:
                if e.errno == errno.EPIPE:
                    sys.stdout = PacifyFlushWrapper(sys.stdout)
                    sys.stderr = PacifyFlushWrapper(sys.stderr)
                    sys.exit(1)
                else:
                    raise
        except Exit as e:
            if standalone_mode:
                sys.exit(e.exit_code)
            else:
                # in non-standalone mode, return the exit code
                # note that this is only reached if `self.invoke` above raises
                # an Exit explicitly -- thus bypassing the check there which
                # would return its result
                # the results of non-standalone execution may therefore be
                # somewhat ambiguous: if there are codepaths which lead to
                # `clime.exit(1)` and to `return 1`, the caller won't be able to
                # tell the difference between the two
                return e.exit_code
        except Abort:
            if not standalone_mode:
                raise
            echo("Aborted!", file=sys.stderr)
            sys.exit(1)

    def _main_shelldone(self, clime_args, prog_name, complete_var=None):
        """Check if the shell is asking for tab completion, process
        that, then exit early. Called from :meth:`main` before the
        program is invoked.

        :param prog_name: Name of the executable in the shell.
        :param complete_var: Name of the environment variable that holds
            the completion instruction. Defaults to
            ``_{PROG_NAME}_COMPLETE``.
        """
        if complete_var is None:
            complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

        instruction = os.environ.get(complete_var)

        if not instruction:
            return

        from .shelldone import shell_complete

        rv = shell_complete(self, clime_args, prog_name, complete_var, instruction)
        _fast_exit(rv)

    def __call__(self, *args, **kwargs):
        """Alias for :meth:`main`."""
        return self.main(*args, **kwargs)


class Command(BaseCommand):
    """Commands are the basic building block of command line interfaces in
    quo.  A basic command handles command line parsing and might dispatch
    more parsing to commands nested below it.

    :param name: the name of the command to use unless a tether overrides it.
    :param context_settings: an optional dictionary with defaults that are
                             passed to the context object.
    :param callback: the callback to invoke.  This is optional.
    :param params: the parameters to register with this command.  This can
                   be either :class:`App` or :class:`Argument` objects.
    :param help: the help string to use for this command.
    :param epilog: like the help string but it's printed at the end of the
                   help page after everything else.
    :param short_help: the short help to use for this command.  This is
                       shown on the command listing of the parent command.
    :param add_autohelp: by default each command registers a ``--help``
                            app.  This can be disabled by this parameter.
    :param no_args_is_help: this controls what happens if no arguments are
                            provided.  This app is disabled by default.
                            If enabled this will add ``--help`` as argument
                            if no arguments are passed
    :param hidden: hide this command from help outputs.

    :param deprecated: issues a message indicating that
                             the command is deprecated.
    """

    def __init__(
        self,
        name,
        context_settings=None,
        callback=None,
        params=None,
        help=None,
        epilog=None,
        short_help=None,
        apps_metavar="[OPTIONS]",
        add_autohelp=True,
        no_args_is_help=False,
        hidden=False,
        deprecated=False,
    ):
        super().__init__(name, context_settings)
        #: the callback to execute when the command fires.  This might be
        #: `None` in which case nothing happens.
        self.callback = callback
        #: the list of parameters for this command in the order they
        #: should show up in the help page and execute.  Eager parameters
        #: will automatically be handled before non eager ones.
        self.params = params or []
        # if a form feed (page break) is found in the help text, truncate help
        # text to the content preceding the first form feed
        if help and "\f" in help:
            help = help.split("\f", 1)[0]
        self.help = help
        self.epilog = epilog
        self.apps_metavar = apps_metavar
        self.short_help = short_help
        self.add_autohelp = add_autohelp
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated

    def to_info_dict(self, clime):
        info_dict = super().to_info_dict(clime)
        info_dict.update(
            params=[param.to_info_dict() for param in self.get_params(clime)],
            help=self.help,
            epilog=self.epilog,
            short_help=self.short_help,
            hidden=self.hidden,
            deprecated=self.deprecated,
        )
        return info_dict

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def get_usage(self, clime):
        """Formats the usage line into a string and returns it.

        Calls :meth:`format_usage` internally.
        """
        formatter = clime.make_formatter()
        self.format_usage(clime, formatter)
        return formatter.getvalue().rstrip("\n")

    def get_params(self, clime):
        rv = self.params
        autohelp = self.get_autohelp(clime)
        if autohelp is not None:
            rv = rv + [autohelp]
        return rv

    def format_usage(self, clime, formatter):
        """Writes the usage line into the formatter.

        This is a low-level method called by :meth:`get_usage`.
        """
        pieces = self.collect_usage_pieces(clime)
        formatter.write_usage(clime.command_path, " ".join(pieces))

    def collect_usage_pieces(self, clime):
        """Returns all the pieces that go into the usage line and returns
        it as a list of strings.
        """
        rv = [self.apps_metavar] if self.apps_metavar else []
        for param in self.get_params(clime):
            rv.extend(param.get_usage_pieces(clime))
        return rv

    def get_autohelp_names(self, clime):
        """Returns the names for the help app."""
        all_names = set(clime.autohelp_names)
        for param in self.params:
            all_names.difference_update(param.opts)
            all_names.difference_update(param.secondary_opts)
        return all_names

    def get_autohelp(self, clime):
        """Returns the help app object."""
        autohelps = self.get_autohelp_names(clime)
        if not autohelps or not self.add_autohelp:
            return

        def show_help(clime, param, value):
            if value and not clime.resilient_parsing:
                echo(clime.get_help(), color=clime.color)
                clime.exit()

        return App(
            autohelps,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help="Show this message and exit.",
        )

    def make_parser(self, clime):
        """Creates the underlying app parser for this command."""
        parser = AppParser(clime)
        for param in self.get_params(clime):
            param.add_to_parser(parser, clime)
        return parser

    def get_help(self, clime):
        """Formats the help into a string and returns it.

        Calls :meth:`format_help` internally.
        """
        formatter = clime.make_formatter()
        self.format_help(clime, formatter)
        return formatter.getvalue().rstrip("\n")

    def get_short_help_str(self, limit=45):
        """Gets short help for the command or makes it by shortening the
        long help string.
        """
        return (
            self.short_help
            or self.help
            and make_default_short_help(self.help, limit)
            or ""
        )

    def format_help(self, clime, formatter):
        """Writes the help into the formatter if it exists.

        This is a low-level method called by :meth:`get_help`.

        This calls the following methods:

        -   :meth:`format_usage`
        -   :meth:`format_help_text`
        -   :meth:`format_apps`
        -   :meth:`format_epilog`
        """
        self.format_usage(clime, formatter)
        self.format_help_text(clime, formatter)
        self.format_apps(clime, formatter)
        self.format_epilog(clime, formatter)

    def format_help_text(self, clime, formatter):
        """Writes the help text to the formatter if it exists."""
        if self.help:
            formatter.write_paragraph()
            with formatter.indentation():
                help_text = self.help
                if self.deprecated:
                    help_text += DEPRECATED_HELP_NOTICE
                formatter.write_text(help_text)
        elif self.deprecated:
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(DEPRECATED_HELP_NOTICE)

    def format_apps(self, clime, formatter):
        """Writes all the apps into the formatter if they exist."""
        opts = []
        for param in self.get_params(clime):
            rv = param.get_help_record(clime)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section("Apps"):
                formatter.write_dl(opts)

    def format_epilog(self, clime, formatter):
        """Writes the epilog into the formatter if it exists."""
        if self.epilog:
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(self.epilog)

    def parse_args(self, clime, args):
        if not args and self.no_args_is_help and not clime.resilient_parsing:
            echo(clime.get_help(), color=clime.color)
            clime.exit()

        parser = self.make_parser(clime)
        opts, args, param_order = parser.parse_args(args=args)

        for param in iter_params_for_processing(param_order, self.get_params(clime)):
            value, args = param.handle_parse_result(clime, opts, args)

        if args and not clime.allow_extra_args and not clime.resilient_parsing:
            clime.fail(
                "Got unexpected extra"
                f" argument{'s' if len(args) != 1 else ''}"
                f" ({' '.join(map(make_str, args))})"
            )

        clime.args = args
        return args

    def invoke(self, clime):
        """Given a context, this invokes the attached callback (if it exists)
        in the right way.
        """
        deprecated_notice(self)
        if self.callback is not None:
            return clime.invoke(self.callback, **clime.params)

    def shell_complete(self, clime, incomplete):
        """Return a list of completions for the incomplete value. Looks
        at the names of apps and chained multi-commands.

        :param clime: Invocation context for this command.
        :param incomplete: Value being completed. May be empty.

        """
        from quo.shelldone import CompletionItem

        results = []

        if incomplete and not incomplete[0].isalnum():
            for param in self.get_params(clime):
                if (
                    not isinstance(param, App)
                    or param.hidden
                    or (
                        not param.multiple
                        and clime.get_parameter_source(param.name)
                        is ParameterSource.COMMANDLINE
                    )
                ):
                    continue

                results.extend(
                    CompletionItem(name, help=param.help)
                    for name in param.opts + param.secondary_opts
                    if name.startswith(incomplete)
                )

        results.extend(super().shell_complete(clime, incomplete))
        return results


class MultiCommand(Command):
    """A multi command is the basic implementation of a command that
    dispatches to subcommands.  The most common version is the
    :class:`Tether`.

    :param invoke_without_command: this controls how the multi command itself
                                   is invoked.  By default it's only invoked
                                   if a subcommand is provided.
    :param no_args_is_help: this controls what happens if no arguments are
                            provided.  This app is enabled by default if
                            `invoke_without_command` is disabled or disabled
                            if it's enabled.  If enabled this will add
                            ``--help`` as argument if no arguments are
                            passed.
    :param subcommand_metavar: the string that is used in the documentation
                               to indicate the subcommand place.
    :param chain: if this is set to `True` chaining of multiple subcommands
                  is enabled.  This restricts the form of commands in that
                  they cannot have optional arguments but it allows
                  multiple commands to be chained together.
    :param result_callback: the result callback to attach to this multi
                            command.
    """

    allow_extra_args = True
    allow_interspersed_args = False

    def __init__(
        self,
        name=None,
        invoke_without_command=False,
        no_args_is_help=None,
        subcommand_metavar=None,
        chain=False,
        result_callback=None,
        **attrs,
    ):
        super().__init__(name, **attrs)
        if no_args_is_help is None:
            no_args_is_help = not invoke_without_command
        self.no_args_is_help = no_args_is_help
        self.invoke_without_command = invoke_without_command
        if subcommand_metavar is None:
            if chain:
                subcommand_metavar = SUBCOMMANDS_METAVAR
            else:
                subcommand_metavar = SUBCOMMAND_METAVAR
        self.subcommand_metavar = subcommand_metavar
        self.chain = chain
        #: The result callback that is stored.  This can be set or
        #: overridden with the :func:`resultcallback` decorator.
        self.result_callback = result_callback

        if self.chain:
            for param in self.params:
                if isinstance(param, Argument) and not param.required:
                    raise RuntimeError(
                        "Multi commands in chain mode cannot have"
                        " optional arguments."
                    )

    def to_info_dict(self, clime):
        info_dict = super().to_info_dict(clime)
        commands = {}

        for name in self.list_commands(clime):
            command = self.get_command(clime, name)
            sub_clime = clime._make_sub_context(command)

            with sub_clime.scope(cleanup=False):
                commands[name] = command.to_info_dict(sub_clime)

        info_dict.update(commands=commands, chain=self.chain)
        return info_dict

    def collect_usage_pieces(self, clime):
        rv = super().collect_usage_pieces(clime)
        rv.append(self.subcommand_metavar)
        return rv

    def format_apps(self, clime, formatter):
        super().format_apps(clime, formatter)
        self.format_commands(clime, formatter)

    def resultcallback(self, replace=False):
        """Adds a result callback to the command.  By default if a
        result callback is already registered this will chain them but
        this can be disabled with the `replace` parameter.  The result
        callback is invoked with the return value of the subcommand
        (or the list of return values from all subcommands if chaining
        is enabled) as well as the parameters as they would be passed
        to the main callback.

        Example::

            @quo.tether()
            @quo.app('-i', '--input', default=23)
            def cli(input):
                return 42

            @cli.resultcallback()
            def process_result(result, input):
                return result + input

        :param replace: if set to `True` an already existing result
                        callback will be removed

        """

        def decorator(f):
            old_callback = self.result_callback
            if old_callback is None or replace:
                self.result_callback = f
                return f

            def function(__value, *args, **kwargs):
                return f(old_callback(__value, *args, **kwargs), *args, **kwargs)

            self.result_callback = rv = update_wrapper(function, f)
            return rv

        return decorator

    def format_commands(self, clime, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the apps.
        """
        commands = []
        for subcommand in self.list_commands(clime):
            cmd = self.get_command(clime, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Commands"):
                    formatter.write_dl(rows)

    def parse_args(self, clime, args):
        if not args and self.no_args_is_help and not clime.resilient_parsing:
            echo(clime.get_help(), color=clime.color)
            clime.exit()

        rest = super().parse_args(clime, args)

        if self.chain:
            clime.protected_args = rest
            clime.args = []
        elif rest:
            clime.protected_args, clime.args = rest[:1], rest[1:]

        return clime.args

    def invoke(self, clime):
        def _process_result(value):
            if self.result_callback is not None:
                value = clime.invoke(self.result_callback, value, **clime.params)
            return value

        if not clime.protected_args:
            if self.invoke_without_command:
                # No subcommand was invoked, so the result callback is
                # invoked with None for regular tethered componentss, or an empty list
                # for chained commandss.
                with clime:
                    super().invoke(clime)
                    return _process_result([] if self.chain else None)
            clime.fail("Missing command.")

        # Fetch args back out
        args = clime.protected_args + clime.args
        clime.args = []
        clime.protected_args = []

        # If we're not in chain mode, we only allow the invocation of a
        # single command but we also inform the current context about the
        # name of the command to invoke.
        if not self.chain:
            # Make sure the context is entered so we do not clean up
            # resources until the result processor has worked.
            with clime:
                cmd_name, cmd, args = self.resolve_command(clime, args)
                clime.invoked_subcommand = cmd_name
                super().invoke(clime)
                sub_clime = cmd.make_context(cmd_name, args, parent=clime)
                with sub_clime:
                    return _process_result(sub_clime.command.invoke(sub_clime))

        # In chain mode we create the contexts step by step, but after the
        # base command has been invoked.  Because at that point we do not
        # know the subcommands yet, the invoked subcommand attribute is
        # set to ``*`` to inform the command that subcommands are executed
        # but nothing else.
        with clime:
            clime.invoked_subcommand = "*" if args else None
            super().invoke(clime)

            # Otherwise we make every single context and invoke them in a
            # chain.  In that case the return value to the result processor
            # is the list of all invoked subcommand's results.
            contexts = []
            while args:
                cmd_name, cmd, args = self.resolve_command(clime, args)
                sub_clime = cmd.make_context(
                    cmd_name,
                    args,
                    parent=clime,
                    allow_extra_args=True,
                    allow_interspersed_args=False,
                )
                contexts.append(sub_clime)
                args, sub_clime.args = sub_clime.args, []

            rv = []
            for sub_clime in contexts:
                with sub_clime:
                    rv.append(sub_clime.command.invoke(sub_clime))
            return _process_result(rv)

    def resolve_command(self, clime, args):
        cmd_name = make_str(args[0])
        original_cmd_name = cmd_name

        # Get the command
        cmd = self.get_command(clime, cmd_name)

        # If we can't find the command but there is a normalization
        # function available, we try with that one.
        if cmd is None and clime.token_normalize_func is not None:
            cmd_name = clime.token_normalize_func(cmd_name)
            cmd = self.get_command(clime, cmd_name)

        # If we don't find the command we want to show an error message
        # to the user that it was not provided.  However, there is
        # something else we should do: if the first argument looks like
        # an app we want to kick off parsing again for arguments to
        # resolve things like --help which now should go to the main
        # place.
        if cmd is None and not clime.resilient_parsing:
            if split_opt(cmd_name)[0]:
                self.parse_args(clime, clime.args)
            clime.fail(f"No such command '{original_cmd_name}'.")
        return cmd.name if cmd else None, cmd, args[1:]

    def get_command(self, clime, cmd_name):
        """Given a context and a command name, this returns a
        :class:`Command` object if it exists or returns `None`.
        """
        raise NotImplementedError()

    def list_commands(self, clime):
        """Returns a list of subcommand names in the order they should
        appear.
        """
        return []

    def shell_complete(self, clime, incomplete):
        """Return a list of completions for the incomplete value. Looks
        at the names of apps, subcommands, and chained
        multi-commands.

        :param clime: Invocation context for this command.
        :param incomplete: Value being completed. May be empty.

        """
        from quo.shelldone import CompletionItem

        results = [
            CompletionItem(name, help=command.get_short_help_str())
            for name, command in _complete_visible_commands(clime, incomplete)
        ]
        results.extend(super().shell_complete(clime, incomplete))
        return results


class Tether(MultiCommand):
    """A tether allows a command to have subcommands attached. This is
    the most common way to implement nesting in quo.

    :param name: The name of the tethered command.
    :param commands: A dict mapping names to :class:`Command` objects.
        Can also be a list of :class:`Command`, which will use
        :attr:`Command.name` to create the dict.
    :param attrs: Other command arguments described in
        :class:`MultiCommand`, :class:`Command`, and
        :class:`BaseCommand`.

    """

    #: If set, this is used by the tether's :meth:`command` decorator
    #: as the default :class:`Command` class. This is useful to make all
    #: subcommands use a custom command class.
    #:
    command_class = None

    #: If set, this is used by the tether's :meth:`tether` decorator
    #: as the default :class:`Tether` class. This is useful to make all
    #: subgroups use a custom tether class.
    #:
    #: If set to the special value :class:`type` (literally
    #: ``group_class = type``), this tether's class will be used as the
    #: default class. This makes a custom tether class continue to make
    #: custom tethered componentss.
    group_class = None

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, **attrs)

        if commands is None:
            commands = {}
        elif isinstance(commands, (list, tuple)):
            commands = {c.name: c for c in commands}

        #: The registered subcommands by their exported names.
        self.commands = commands

    def addcommand(self, cmd, name=None):
        """Registers another :class:`Command` with this tether.  If the name
        is not provided, the name of the command is used.
        """
        name = name or cmd.name
        if name is None:
            raise TypeError("Command has no name.")
        multicommand_checker(self, name, cmd, register=True)
        self.commands[name] = cmd

    def command(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a decree(command) to
        the tether. This takes the same arguments as :func:`command` and
        immediately registers the created command with this tether by
        calling :meth:`addcommand`.

        To customize the command class used, set the
        :attr:`command_class` attribute.

        """
        from quo.decorators.core import command

        if self.command_class is not None and "cls" not in kwargs:
            kwargs["cls"] = self.command_class

        def decorator(f):
            cmd = command(*args, **kwargs)(f)
            self.addcommand(cmd)
            return cmd

        return decorator

    def tether(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a tether to the tether. This takes the same arguments as :func:`tether` and immediately registers the created tether with this tether by calling :meth:`addcommand`.

        To customize the tether class used, set the :attr:`group_class` attribute.

        """
        from quo.decorators.core import tether

        if self.group_class is not None and "cls" not in kwargs:
            if self.group_class is type:
                kwargs["cls"] = type(self)
            else:
                kwargs["cls"] = self.group_class

        def decorator(f):
            cmd = group(*args, **kwargs)(f)
            self.addcommand(cmd)
            return cmd

        return decorator

    def get_command(self, clime, cmd_name):
        return self.commands.get(cmd_name)

    def list_commands(self, clime):
        return sorted(self.commands)


class CommandCollection(MultiCommand):
    """A command collection is a multi command that merges multiple multi
    commands together into one.  This is a straightforward implementation
    that accepts a list of different multi commands as sources and
    provides all the commands for each of them.
    """

    def __init__(self, name=None, sources=None, **attrs):
        super().__init__(name, **attrs)
        #: The list of registered multi commands.
        self.sources = sources or []

    def add_source(self, multi_cmd):
        """Adds a new multi command to the chain dispatcher."""
        self.sources.append(multi_cmd)

    def get_command(self, clime, cmd_name):
        for source in self.sources:
            rv = source.get_command(clime, cmd_name)
            if rv is not None:
                if self.chain:
                    multicommand_checker(self, cmd_name, rv)
                return rv

    def list_commands(self, clime):
        rv = set()
        for source in self.sources:
            rv.update(source.list_commands(clime))
        return sorted(rv)


class Parameter:
    r"""A parameter to a command comes in two versions: they are either
    :class:`App`\s or :class:`Argument`\s.  Other subclasses are currently
    not supported by design as some of the internals for parsing are
    intentionally not finalized.

    Some settings are supported by both apps and arguments.

    :param param_decls: the parameter declarations for this app or
                        argument.  This is a list of flags or argument
                        names.
    :param type: the type that should be used.  Either a :class:`ParamType`
                 or a Python type.  The later is converted into the former
                 automatically if supported.
    :param required: controls if this is optional or not.
    :param default: the default value if omitted.  This can also be a callable,
                    in which case it's invoked when the default is needed
                    without any arguments.
    :param callback: a callback that should be executed after the parameter
                     was matched.  This is called as ``fn(clime, param,
                     value)`` and needs to return the value.
    :param nargs: the number of arguments to match.  If not ``1`` the return
                  value is a tuple instead of single value.  The default for
                  nargs is ``1`` (except if the type is a tuple, then it's
                  the arity of the tuple). If ``nargs=-1``, all remaining
                  parameters are collected.
    :param metavar: how the value is represented in the help page.
    :param expose_value: if this is `True` then the value is passed onwards
                         to the command callback and stored on the context,
                         otherwise it's skipped.
    :param is_eager: eager values are processed before non eager ones.  This
                     should not be set for arguments or it will inverse the
                     order of processing.
    :param envvar: a string or list of strings that are environment variables
                   that should be checked.
    :param shell_complete: A function that returns custom shell
        completions. Used instead of the param's type completion if
        given. Takes ``clime, param, incomplete`` and must return a list
        of :class:`~quo.shelldone.CompletionItem` or a list of
        strings.

    """

    param_type_name = "parameter"

    def __init__(
        self,
        param_decls=None,
        type=None,
        required=False,
        default=None,
        callback=None,
        nargs=None,
        metavar=None,
        expose_value=True,
        is_eager=False,
        envvar=None,
        shell_complete=None,
        autocompletion=None,
    ):
        self.name, self.opts, self.secondary_opts = self._parse_decls(
            param_decls or (), expose_value
        )

        self.type = convert_type(type, default)

        # Default nargs to what the type tells us if we have that
        # information available.
        if nargs is None:
            if self.type.is_composite:
                nargs = self.type.arity
            else:
                nargs = 1

        self.required = required
        self.callback = callback
        self.nargs = nargs
        self.multiple = False
        self.expose_value = expose_value
        self.default = default
        self.is_eager = is_eager
        self.metavar = metavar
        self.envvar = envvar

        if autocompletion is not None:
        

            def shell_complete(clime, param, incomplete):
                from quo.shelldone import CompletionItem

                out = []

                for c in autocompletion(clime, [], incomplete):
                    if isinstance(c, tuple):
                        c = CompletionItem(c[0], help=c[1])
                    elif isinstance(c, str):
                        c = CompletionItem(c)

                    if c.value.startswith(incomplete):
                        out.append(c)

                return out

        self._custom_shell_complete = shell_complete

    def to_info_dict(self):
        """Gather information that could be useful for a tool generating
        user-facing documentation.

        Use :meth:`quo.Context.to_info_dict` to traverse the entire
        CLI structure 

        """
        return {
            "name": self.name,
            "param_type_name": self.param_type_name,
            "opts": self.opts,
            "secondary_opts": self.secondary_opts,
            "type": self.type.to_info_dict(),
            "required": self.required,
            "nargs": self.nargs,
            "multiple": self.multiple,
            "default": self.default,
            "envvar": self.envvar,
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @property
    def human_readable_name(self):
        """Returns the human readable name of this parameter.  This is the
        same as the name for apps, but the metavar for arguments.
        """
        return self.name

    def make_metavar(self):
        if self.metavar is not None:
            return self.metavar
        metavar = self.type.get_metavar(self)
        if metavar is None:
            metavar = self.type.name.upper()
        if self.nargs != 1:
            metavar += "..."
        return metavar

    def get_default(self, clime, call=True):
        """Get the default for the parameter. Tries
        :meth:`Context.lookup_value` first, then the local default.

        :param clime: Current context.
        :param call: If the default is a callable, call it.
        Disable to return the callable instead.
        Looks at ``clime.default_map`` first. Added the ``call``        parameter.
        """
        value = clime.lookup_default(self.name, call=False)

        if value is None:
            value = self.default

        if callable(value):
            if not call:
                # Don't type cast the callable.
                return value

            value = value()

        return self.type_cast_value(clime, value)

    def add_to_parser(self, parser, clime):
        pass

    def consume_value(self, clime, opts):
        value = opts.get(self.name)
        source = ParameterSource.COMMANDLINE

        if value is None:
            value = self.value_from_envvar(clime)
            source = ParameterSource.ENVIRONMENT

        if value is None:
            value = clime.lookup_default(self.name)
            source = ParameterSource.DEFAULT_MAP

        if value is None:
            value = self.get_default(clime)
            source = ParameterSource.DEFAULT

        return value, source

    def type_cast_value(self, clime, value):
        """Given a value this runs it properly through the type system. This automatically handles things like `nargs` and `multiple` as  well as composite types.
        """
        if value is None:
            return () if self.multiple or self.nargs == -1 else None

        if self.type.is_composite:
            if self.nargs <= 1:
                raise TypeError(
                    "Attempted to invoke composite type but nargs has"
                    f" been set to {self.nargs}. This is not supported;"
                    " nargs needs to be set to a fixed value > 1."
                )

            if self.multiple:
                return tuple(self.type(x, self, clime) for x in value)

            return self.type(value, self, clime)

        def _convert(value, level):
            if level == 0:
                return self.type(value, self, clime)

            return tuple(_convert(x, level - 1) for x in value)

        return _convert(value, (self.nargs != 1) + bool(self.multiple))

    def process_value(self, clime, value):
        """Given a value and context this runs the logic to convert the
        value as necessary.
        """
        # If the value we were given is None we do nothing.  This way
        # code that calls this can easily figure out if something was
        # not provided.  Otherwise it would be converted into an empty
        # tuple for multiple invocations which is inconvenient.
        if value is not None:
            return self.type_cast_value(clime, value)

    def value_is_missing(self, value):
        if value is None:
            return True
        if (self.nargs != 1 or self.multiple) and value == ():
            return True
        return False

    def full_process_value(self, clime, value):
        value = self.process_value(clime, value)

        if self.required and self.value_is_missing(value):
            raise MissingParameter(clime=clime, param=self)

        # For bounded nargs (!= -1), validate the number of values.
        if (
            not clime.resilient_parsing
            and self.nargs > 1
            and isinstance(value, (tuple, list))
            and (
                any(len(v) != self.nargs for v in value)
                if self.multiple
                else len(value) != self.nargs
            )
        ):
            were = "was" if len(value) == 1 else "were"
            clime.fail(
                f"Argument {self.name!r} takes {self.nargs} values but"
                f" {len(value)} {were} given."
            )

        return value

    def resolve_envvar_value(self, clime):
        if self.envvar is None:
            return

        if isinstance(self.envvar, (tuple, list)):
            for envvar in self.envvar:
                rv = os.environ.get(envvar)

                if rv:
                    return rv
        else:
            rv = os.environ.get(self.envvar)

            if rv:
                return rv

    def value_from_envvar(self, clime):
        rv = self.resolve_envvar_value(clime)

        if rv is not None and self.nargs != 1:
            rv = self.type.split_envvar_value(rv)

        return rv

    def handle_parse_result(self, clime, opts, args):
        with augment_usage_errors(clime, param=self):
            value, source = self.consume_value(clime, opts)
            clime.set_parameter_source(self.name, source)

            try:
                value = self.full_process_value(clime, value)

                if self.callback is not None:
                    value = self.callback(clime, self, value)
            except Exception:
                if not clime.resilient_parsing:
                    raise

                value = None

        if self.expose_value:
            clime.params[self.name] = value

        return value, args

    def get_help_record(self, clime):
        pass

    def get_usage_pieces(self, clime):
        return []

    def get_error_hint(self, clime):
        """Get a stringified version of the param for use in error messages to
        indicate which param caused the error.
        """
        hint_list = self.opts or [self.human_readable_name]
        return " / ".join(repr(x) for x in hint_list)

    def shell_complete(self, clime, incomplete):
        """Return a list of completions for the incomplete value. If a
        ``shell_complete`` function was given during init, it is used.
        Otherwise, the :attr:`type`
        :meth:`~quo.types.ParamType.shell_complete` function is used.

        :param clime: Invocation context for this command.
        :param incomplete: Value being completed. May be empty

        """
        if self._custom_shell_complete is not None:
            results = self._custom_shell_complete(clime, self, incomplete)

            if results and isinstance(results[0], str):
                from quo.shelldone import CompletionItem

                results = [CompletionItem(c) for c in results]

            return results

        return self.type.shell_complete(clime, self, incomplete)


class App(Parameter):
    """Apps are usually optional values on the command line and
    have some extra features that arguments don't have.

    All other parameters are passed onwards to the parameter constructor.

    :param show_default: controls if the default value should be shown on the
                         help page. Normally, defaults are not shown. If this
                         value is a string, it shows the string instead of the
                         value. This is particularly useful for dynamic apps.
    :param show_envvar: controls if an environment variable should be shown on
                        the help page.  Normally, environment variables
                        are not shown.
    :param prompt: if set to `True` or a non empty string then the user will be
                   prompted for input.  If set to `True` the prompt will be the
                   app name capitalized.
    :param autoconfirm: if set then the value will need to be confirmed
                                if it was prompted for.
    :param prompt_required: If set to ``False``, the user will be
        prompted for input only when the app was specified as a flag
        without a value.
    :param hide_input: if this is `True` then the input on the prompt will be
                       hidden from the user.  This is useful for password
                       input.
    :param is_flag: forces this app to act as a flag.  The default is
                    auto detection.
    :param flag_value: which value should be used for this flag if it's
                       enabled.  This is set to a boolean automatically if
                       the app string contains a slash to mark two apps.
    :param multiple: if this is set to `True` then the argument is accepted
                     multiple times and recorded.  This is similar to ``nargs``
                     in how it works but supports arbitrary number of
                     arguments.
    :param count: this flag makes an app increment an integer.
    :param allow_from_autoenv: if this is enabled then the value of this
                               parameter will be pulled from an environment
                               variable in case a prefix is defined on the
                               context.
    :param help: the help string.
    :param hidden: hide this option from help outputs.
    """

    param_type_name = "app"

    def __init__(
        self,
        param_decls=None,
        show_default=False,
        prompt=False,
        autoconfirm=False,
        prompt_required=True,
        hide=False,
        is_flag=None,
        flag_value=None,
        multiple=False,
        count=False,
        allow_from_autoenv=True,
        type=None,
        help=None,
        hidden=False,
        show_choices=True,
        show_envvar=False,
        **attrs,
    ):
        default_is_missing = attrs.get("default", _missing) is _missing
        super().__init__(param_decls, type=type, **attrs)

        if prompt is True:
            prompt_text = self.name.replace("_", " ").capitalize()
        elif prompt is False:
            prompt_text = None
        else:
            prompt_text = prompt
        self.prompt = prompt_text
        self.autoconfirm = autoconfirm
        self.prompt_required = prompt_required
        self.hide = hide
        self.hidden = hidden

        # If prompt is enabled but not required, then the app can be
        # used as a flag to indicate using prompt or flag_value.
        self._flag_needs_value = self.prompt is not None and not self.prompt_required

        if is_flag is None:
            if flag_value is not None:
                # Implicitly a flag because flag_value was set.
                is_flag = True
            elif self._flag_needs_value:
                # Not a flag, but when used as a flag it shows a prompt.
                is_flag = False
            else:
                # Implicitly a flag because flag apps were given.
                is_flag = bool(self.secondary_opts)
        elif is_flag is False and not self._flag_needs_value:
            # Not a flag, and prompt is not enabled, can be used as a
            # flag if flag_value is set.
            self._flag_needs_value = flag_value is not None

        if is_flag and default_is_missing:
            self.default = False

        if flag_value is None:
            flag_value = not self.default

        self.is_flag = is_flag
        self.flag_value = flag_value

        if self.is_flag and isinstance(self.flag_value, bool) and type in [None, bool]:
            self.type = BOOL
            self.is_bool_flag = True
        else:
            self.is_bool_flag = False

        # Counting
        self.count = count
        if count:
            if type is None:
                self.type = IntRange(min=0)
            if default_is_missing:
                self.default = 0

        self.multiple = multiple
        self.allow_from_autoenv = allow_from_autoenv
        self.help = help
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar

        # Sanity check for stuff we don't support
        if __debug__:
            if self.nargs < 0:
                raise TypeError("Apps cannot have nargs < 0")
            if self.prompt and self.is_flag and not self.is_bool_flag:
                raise TypeError("Cannot prompt for flags that are not bools.")
            if not self.is_bool_flag and self.secondary_opts:
                raise TypeError("Got secondary app for non boolean flag.")
            if self.is_bool_flag and self.hide and self.prompt is not None:
                raise TypeError("Hidden input does not work with boolean flag prompts.")
            if self.count:
                if self.multiple:
                    raise TypeError(
                        "Apps cannot be multiple and count at the same time."
                    )
                elif self.is_flag:
                    raise TypeError(
                        "Apps cannot be count and flags at the same time."
                    )

    def to_info_dict(self):
        info_dict = super().to_info_dict()
        info_dict.update(
            help=self.help,
            prompt=self.prompt,
            is_flag=self.is_flag,
            flag_value=self.flag_value,
            count=self.count,
            hidden=self.hidden,
        )
        return info_dict

    def _parse_decls(self, decls, expose_value):
        opts = []
        secondary_opts = []
        name = None
        possible_names = []

        for decl in decls:
            if decl.isidentifier():
                if name is not None:
                    raise TypeError("Name defined twice")
                name = decl
            else:
                split_char = ";" if decl[:1] == "/" else "/"
                if split_char in decl:
                    first, second = decl.split(split_char, 1)
                    first = first.rstrip()
                    if first:
                        possible_names.append(split_opt(first))
                        opts.append(first)
                    second = second.lstrip()
                    if second:
                        secondary_opts.append(second.lstrip())
                    if first == second:
                        raise ValueError(
                            f"Boolean app {decl!r} cannot use the"
                            " same flag for true/false."
                        )
                else:
                    possible_names.append(split_opt(decl))
                    opts.append(decl)

        if name is None and possible_names:
            possible_names.sort(key=lambda x: -len(x[0]))  # group long apps first
            name = possible_names[0][1].replace("-", "_").lower()
            if not name.isidentifier():
                name = None

        if name is None:
            if not expose_value:
                return None, opts, secondary_opts
            raise TypeError("Could not determine name for app")

        if not opts and not secondary_opts:
            raise TypeError(
                f"No apps defined but a name was passed ({name})."
                " Did you mean to declare an argument instead? Did"
                f" you mean to pass '--{name}'?"
            )

        return name, opts, secondary_opts

    def add_to_parser(self, parser, clime):
        kwargs = {
            "dest": self.name,
            "nargs": self.nargs,
            "obj": self,
        }

        if self.multiple:
            action = "append"
        elif self.count:
            action = "count"
        else:
            action = "store"

        if self.is_flag:
            kwargs.pop("nargs", None)
            action_const = f"{action}_const"
            if self.is_bool_flag and self.secondary_opts:
                parser.add_app(self.opts, action=action_const, const=True, **kwargs)
                parser.add_app(
                    self.secondary_opts, action=action_const, const=False, **kwargs
                )
            else:
                parser.add_app(
                    self.opts, action=action_const, const=self.flag_value, **kwargs
                )
        else:
            kwargs["action"] = action
            parser.add_app(self.opts, **kwargs)

    def get_help_record(self, clime):
        if self.hidden:
            return
        any_prefix_is_slash = []

        def _write_opts(opts):
            rv, any_slashes = join_apps(opts)
            if any_slashes:
                any_prefix_is_slash[:] = [True]
            if not self.is_flag and not self.count:
                rv += f" {self.make_metavar()}"
            return rv

        rv = [_write_opts(self.opts)]
        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ""
        extra = []
        if self.show_envvar:
            envvar = self.envvar
            if envvar is None:
                if self.allow_from_autoenv and clime.auto_envvar_prefix is not None:
                    envvar = f"{clime.auto_envvar_prefix}_{self.name.upper()}"
            if envvar is not None:
                var_str = (
                    ", ".join(str(d) for d in envvar)
                    if isinstance(envvar, (list, tuple))
                    else envvar
                )
                extra.append(f"env var: {var_str}")

        default_value = self.get_default(clime, call=False)

        if default_value is not None and (self.show_default or clime.show_default):
            if isinstance(self.show_default, str):
                default_string = f"({self.show_default})"
            elif isinstance(default_value, (list, tuple)):
                default_string = ", ".join(str(d) for d in default_value)
            elif callable(default_value):
                default_string = "(dynamic)"
            elif self.is_bool_flag and self.secondary_opts:
                # For boolean flags that have distinct True/False opts,
                # use the opt without prefix instead of the value.
                default_string = split_opt(
                    (self.opts if self.default else self.secondary_opts)[0]
                )[1]
            else:
                default_string = default_value

            extra.append(f"default: {default_string}")

        if isinstance(self.type, _NumberRangeBase):
            range_str = self.type._describe_range()

            if range_str:
                extra.append(range_str)

        if self.required:
            extra.append("required")
        if extra:
            extra_str = ";".join(extra)
            help = f"{help}  [{extra_str}]" if help else f"[{extra_str}]"

        return ("; " if any_prefix_is_slash else " / ").join(rv), help

    def get_default(self, clime, call=True):
        # If we're a non boolean flag our default is more complex because
        # we need to look at all flags in the same tether to figure out
        # if we're the the default one in which case we return the flag
        # value as default.
        if self.is_flag and not self.is_bool_flag:
            for param in clime.command.params:
                if param.name == self.name and param.default:
                    return param.flag_value

            return None

        return super().get_default(clime, call=call)

    def prompt_for_value(self, clime):
        """This is an alternative flow that can be activated in the full
        value processing if a value does not exist.  It will prompt the
        user until a valid value exists and then returns the processed
        value as result.
        """
        # Calculate the default before prompting anything to be stable.
        default = self.get_default(clime)

        # If this is a prompt for a flag we need to handle this
        # differently.
        if self.is_bool_flag:
            return confirm(self.prompt, default)

        return prompt(
            self.prompt,
            default=default,
            type=self.type,
            hide=self.hide,
            show_choices=self.show_choices,
            autoconfirm=self.autoconfirm,
            value_proc=lambda x: self.process_value(clime, x),
        )

    def resolve_envvar_value(self, clime):
        rv = super().resolve_envvar_value(clime)

        if rv is not None:
            return rv

        if self.allow_from_autoenv and clime.auto_envvar_prefix is not None:
            envvar = f"{clime.auto_envvar_prefix}_{self.name.upper()}"
            rv = os.environ.get(envvar)

            if rv:
                return rv

    def value_from_envvar(self, clime):
        rv = self.resolve_envvar_value(clime)

        if rv is None:
            return None

        value_depth = (self.nargs != 1) + bool(self.multiple)

        if value_depth > 0 and rv is not None:
            rv = self.type.split_envvar_value(rv)

            if self.multiple and self.nargs != 1:
                rv = batch(rv, self.nargs)

        return rv

    def consume_value(self, clime, opts):
        value, source = super().consume_value(clime, opts)

        # The parser will emit a sentinel value if the app can be
        # given as a flag without a value. This is different from None
        # to distinguish from the flag not being given at all.
        if value is _flag_needs_value:
            if self.prompt is not None and not clime.resilient_parsing:
                value = self.prompt_for_value(clime)
                source = ParameterSource.PROMPT
            else:
                value = self.flag_value
                source = ParameterSource.COMMANDLINE

        # The value wasn't set, or used the param's default, prompt if
        # prompting is enabled.
        elif (
            source in {None, ParameterSource.DEFAULT}
            and self.prompt is not None
            and (self.required or self.prompt_required)
            and not clime.resilient_parsing
        ):
            value = self.prompt_for_value(clime)
            source = ParameterSource.PROMPT

        return value, source


class Arg(Parameter):
    """Args are positional parameters(arguments to a command.  They generally  provide fewer features than apps but can have infinite ``nargs`` and are required by default.
 All parameters are passed onwards to the parameter constructor.
    """

    param_type_name = "arg"

    def __init__(self, param_decls, required=None, **attrs):
        if required is None:
            if attrs.get("default") is not None:
                required = False
            else:
                required = attrs.get("nargs", 1) > 0

        super().__init__(param_decls, required=required, **attrs)

        if self.default is not None and self.nargs < 0:
            raise TypeError(
                "nargs=-1 in combination with a default value is not supported."
            )

    @property
    def human_readable_name(self):
        if self.metavar is not None:
            return self.metavar
        return self.name.upper()

    def make_metavar(self):
        if self.metavar is not None:
            return self.metavar
        var = self.type.get_metavar(self)
        if not var:
            var = self.name.upper()
        if not self.required:
            var = f"[{var}]"
        if self.nargs != 1:
            var += "..."
        return var

    def _parse_decls(self, decls, expose_value):
        if not decls:
            if not expose_value:
                return None, [], []
            raise TypeError("Could not determine name for arg")
        if len(decls) == 1:
            name = arg = decls[0]
            name = name.replace("-", "_").lower()
        else:
            raise TypeError(
                "Args take exactly one parameter declaration, got"
                f" {len(decls)}."
            )
        return name, [arg], []

    def get_usage_pieces(self, clime):
        return [self.make_metavar()]

    def get_error_hint(self, clime):
        return repr(self.make_metavar())

def add_to_parser(self, parser, clime):
        parser.add_argument(dest=self.name, nargs=self.nargs, obj=self)
