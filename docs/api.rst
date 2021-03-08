API
===

.. module:: quo

This part of the documentation lists the full API reference of all public
classes and functions.

Decorators
----

-------
command
-------
 
quo.command(name=None, cls=None, **attrs)
Creates a new Command and uses the decorated function as callback. This will also automatically attach all decorated option()s and argument()s as parameters to the command.

The name of the command defaults to the name of the function with underscores replaced by dashes. If you want to change that, you can pass the intended name as the first argument.

All keyword arguments are forwarded to the underlying command class.

Once decorated the function turns into a Command instance that can be invoked as a command line utility or be attached to a command Group.

Parameters
name – the name of the command. This defaults to the function name with underscores replaced by dashes.

cls – the command class to instantiate. This defaults to Command.

------
group
------

click.group(name=None, **attrs)
Creates a new Group with a function as callback. This works otherwise the same as command() just that the cls parameter is set to Group.

---------
argument
---------
click.argument(*param_decls, **attrs)
Attaches an argument to the command. All positional arguments are passed as parameter declarations to Argument; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Argument instance manually and attaching it to the Command.params list.

Parameters
cls – the argument class to instantiate. This defaults to Argument.

---------
option
---------
click.option(*param_decls, **attrs)
Attaches an option to the command. All positional arguments are passed as parameter declarations to Option; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Option instance manually and attaching it to the Command.params list.

Parameters
cls – the option class to instantiate. This defaults to Option.

----------
autopswd
----------
click.password_option(*param_decls, **attrs)
Shortcut for password prompts.

This is equivalent to decorating a function with option() with the following parameters:

@click.command()
@click.option('--password', prompt=True, confirmation_prompt=True,
              hide_input=True)
def changeadmin(password):
    pass

-------------
autoconfirm
-------------
click.confirmation_option(*param_decls, **attrs)
Shortcut for confirmation prompts that can be ignored by passing --yes as parameter.

This is equivalent to decorating a function with option() with the following parameters:

def callback(ctx, param, value):
    if not value:
        ctx.abort()

@click.command()
@click.option('--yes', is_flag=True, callback=callback,
              expose_value=False, prompt='Do you want to continue?')
def dropdb():
    pass
click.version_option(version=None, *param_decls, **attrs)
Adds a --version option which immediately ends the program printing out the version number. This is implemented as an eager option that prints the version and exits the program in the callback.

Parameters
version – the version number to show. If not provided Click attempts an auto discovery via setuptools.

prog_name – the name of the program (defaults to autodetection)

message – custom message to show instead of the default ('%(prog)s, version %(version)s')

others – everything else is forwarded to option().

click.help_option(*param_decls, **attrs)
Adds a --help option which immediately ends the program printing out the help page. This is usually unnecessary to add as this is added by default to all commands unless suppressed.

Like version_option(), this is implemented as eager option that prints in the callback and exits.

All arguments are forwarded to option().

click.pass_context(f)¶
Marks a callback as wanting to receive the current context object as first argument.

click.pass_obj(f)
Similar to pass_context(), but only pass the object on the context onwards (Context.obj). This is useful if that object represents the state of a nested system.

click.make_pass_decorator(object_type, ensure=False)
Given an object type this creates a decorator that will work similar to pass_obj() but instead of passing the object of the current context, it will find the innermost context of type object_type().

This generates a decorator that works roughly like this:

from functools import update_wrapper

def decorator(f):
    @pass_context
    def new_func(ctx, *args, **kwargs):
        obj = ctx.find_object(object_type)
        return ctx.invoke(f, obj, *args, **kwargs)
    return update_wrapper(new_func, f)
return decorator
Parameters
object_type – the type of the object to pass.

ensure – if set to True, a new object will be created and remembered on the context if it’s not there yet.

Utilities

.. autofunction:: argument

.. autofunction:: option

.. autofunction:: autopswd

.. autofunction:: autoconfirm

.. autofunction:: autoversion

.. autofunction:: autohelp

.. autofunction:: pass_context

.. autofunction:: pass_obj

.. autofunction:: make_pass_decorator

Utilities
---------

.. autofunction:: echo

.. autofunction:: scrollable

.. autofunction:: prompt

.. autofunction:: confirm

.. autofunction:: progressbar

.. autofunction:: clear

.. autofunction:: style

.. autofunction:: unstyle

.. autofunction:: flair

.. autofunction:: edit

.. autofunction:: launch

.. autofunction:: interpose

.. autofunction:: pause

.. autofunction:: terminalsize

.. autofunction:: get_binary_stream

.. autofunction:: get_text_stream

.. autofunction:: open_file

.. autofunction:: get_app_dir

.. autofunction:: format_filename

Commands
--------

.. autoclass:: BaseCommand
   :members:

.. autoclass:: Command
   :members:

.. autoclass:: MultiCommand
   :members:

.. autoclass:: Group
   :members:

.. autoclass:: CommandCollection
   :members:

Parameters
----------

.. autoclass:: Parameter
   :members:

.. autoclass:: Option

.. autoclass:: Argument

Context
-------

.. autoclass:: Context
   :members:

.. autofunction:: get_current_context

.. autoclass:: quo.core.ParameterSource
    :members:
    :member-order: bysource


Types
-----

.. autodata:: STRING

.. autodata:: INT

.. autodata:: FLOAT

.. autodata:: BOOL

.. autodata:: UUID

.. autodata:: UNPROCESSED

.. autoclass:: File

.. autoclass:: Path

.. autoclass:: Choice

.. autoclass:: IntRange

.. autoclass:: FloatRange

.. autoclass:: Tuple

.. autoclass:: ParamType
   :members:

Exceptions
----------

.. autoexception:: QuoException

.. autoexception:: Abort

.. autoexception:: UsageError

.. autoexception:: BadParameter

.. autoexception:: FileError

.. autoexception:: NoSuchOption

.. autoexception:: BadOptionUsage

.. autoexception:: BadArgumentUsage

Formatting
----------

.. autoclass:: HelpFormatter
   :members:

.. autofunction:: wrap_text

Parsing
-------

.. autoclass:: OptionParser
   :members:


Shell Completion
----------------

See :doc:`/shell-completion` for information about enabling and
customizing Quo's shell completion system.

.. currentmodule:: quo.shell_completion

.. autoclass:: CompletionItem

.. autoclass:: ShellComplete
    :members:
    :member-order: bysource

.. autofunction:: add_completion_class


Testing
-------

.. currentmodule:: quo.testing

.. autoclass:: CliRunner
   :members:

.. autoclass:: Result
   :members:
