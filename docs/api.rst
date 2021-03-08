API
===

.. module:: quo

This part of the documentation lists the full API reference of all public
classes and functions.

Decorators
----

:: command

 quo.command(name=None, cls=None, **attrs)
Creates a new Command and uses the decorated function as callback. This will also automatically attach all decorated option()s and argument()s as parameters to the command.

The name of the command defaults to the name of the function with underscores replaced by dashes. If you want to change that, you can pass the intended name as the first argument.

All keyword arguments are forwarded to the underlying command class.

Once decorated the function turns into a Command instance that can be invoked as a command line utility or be attached to a command Group.

Parameters
name – the name of the command. This defaults to the function name with underscores replaced by dashes.

cls – the command class to instantiate. This defaults to Command.

.. autofunction:: group

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
