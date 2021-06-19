API
===

.. module:: quo

This part of the documentation lists the full API reference of all public
classes and functions.

Decorators
----------

``quo.command`` (name=None, cls=None, **attrs)
Creates a new Command and uses the decorated function as callback. This will also automatically attach all decorated option()s and argument()s as parameters to the command.

The name of the command defaults to the name of the function with underscores replaced by dashes. If you want to change that, you can pass the intended name as the first argument.

All keyword arguments are forwarded to the underlying command class.

Once decorated the function turns into a Command instance that can be invoked as a command line utility or be attached to a command Group.

Parameters
name – the name of the command. This defaults to the function name with underscores replaced by dashes.

cls – the command class to instantiate. This defaults to Command.

``quo.group`` (name=None, **attrs)
Creates a new Group with a function as callback. This works otherwise the same as command() just that the cls parameter is set to Group.

``quo.argument`` (*param_decls, **attrs)
Attaches an argument to the command. All positional arguments are passed as parameter declarations to Argument; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Argument instance manually and attaching it to the Command.params list.

Parameters
cls – the argument class to instantiate. This defaults to Argument.

``quo.option`` (*param_decls, **attrs)
Attaches an option to the command. All positional arguments are passed as parameter declarations to Option; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Option instance manually and attaching it to the Command.params list.

Parameters
cls – the option class to instantiate. This defaults to Option.

``quo.password_option`` (*param_decls, **attrs)
Shortcut for password prompts.

This is equivalent to decorating a function with option() with the following parameters:

@quo.command()
@quo.option('--password', prompt=True, confirmation_prompt=True,
              hide_input=True)
def changeadmin(password):
    pass
``quo.confirmation_option`` (*param_decls, **attrs)
Shortcut for confirmation prompts that can be ignored by passing --yes as parameter.

This is equivalent to decorating a function with option() with the following parameters:

def callback(ctx, param, value):
    if not value:
        ctx.abort()

@quo.command()
@quo.option('--yes', is_flag=True, callback=callback,
              expose_value=False, prompt='Do you want to continue?')
def dropdb():
    pass
``quo.version_option`` (version=None, *param_decls, **attrs)
Adds a --version option which immediately ends the program printing out the version number. This is implemented as an eager option that prints the version and exits the program in the callback.

Parameters
version – the version number to show. If not provided quo attempts an auto discovery via setuptools.

prog_name – the name of the program (defaults to autodetection)

message – custom message to show instead of the default ('%(prog)s, version %(version)s')

others – everything else is forwarded to option().

``quo.help_option`` (*param_decls, **attrs)
Adds a --help option which immediately ends the program printing out the help page. This is usually unnecessary to add as this is added by default to all commands unless suppressed.

Like version_option(), this is implemented as eager option that prints in the callback and exits.

All arguments are forwarded to option().

quo.pass_context(f)
Marks a callback as wanting to receive the current context object as first argument.

quo.pass_obj(f)
Similar to pass_context(), but only pass the object on the context onwards (Context.obj). This is useful if that object represents the state of a nested system.

``quo.make_pass_decorator`` (object_type, ensure=False)
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

.. autofunction:: command

.. autofunction:: group

.. autofunction:: argument

.. autofunction:: option

.. autofunction:: autopswd

.. autofunction:: autoconfirm

.. autofunction:: autoversion

.. autofunction:: autohelp

.. autofunction:: contextualize

.. autofunction:: objectualize

.. autofunction:: make_pass_decorator

.. autofunction:: quo.decorators.pass_meta_key


Utilities
---------

quo.echo(message=None, file=None, nl=True, err=False, color=None)
Prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode and binary data that does not fail no matter how badly configured the system is.

Primarily it means that you can print binary data as well as Unicode data on both 2.x and 3.x to the given file in the most appropriate way possible. This is a very carefree function in that it will try its best to not fail. As of quo 6.0 this includes support for unicode output on the Windows console.

In addition to that, if colorama is installed, the echo function will also support clever handling of ANSI codes. Essentially it will then do the following:

add transparent handling of ANSI color codes on Windows.

hide ANSI codes automatically if the destination file is not a terminal.

Changelog
Parameters
message – the message to print

file – the file to write to (defaults to stdout)

err – if set to true the file defaults to stderr instead of stdout. This is faster and easier than calling get_text_stderr() yourself.

nl – if set to True (the default) a newline is printed afterwards.

color – controls if the terminal supports ANSI colors or not. The default is autodetection.

quo.echo_via_pager(text_or_generator, color=None)
This function takes a text and shows it via an environment specific pager on stdout.

Changelog
Parameters
text_or_generator – the text to page, or alternatively, a generator emitting the text to page.

color – controls if the pager supports ANSI colors or not. The default is autodetection.

quo.prompt(text, default=None, hide_input=False, confirmation_prompt=False, type=None, value_proc=None, prompt_suffix=': ', show_default=True, err=False, show_choices=True)
Prompts a user for input. This is a convenience function that can be used to prompt a user for input later.

If the user aborts the input by sending a interrupt signal, this function will catch it and raise a Abort exception.

New in version 7.0: Added the show_choices parameter.

Changelog
Parameters
text – the text to show for the prompt.

default – the default value to use if no input happens. If this is not given it will prompt until it’s aborted.

hide_input – if this is set to true then the input value will be hidden.

confirmation_prompt – asks for confirmation for the value.

type – the type to use to check the value against.

value_proc – if this parameter is provided it’s a function that is invoked instead of the type conversion to convert a value.

prompt_suffix – a suffix that should be added to the prompt.

show_default – shows or hides the default value in the prompt.

err – if set to true the file defaults to stderr instead of stdout, the same as with echo.

show_choices – Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is “Group by” then the prompt will be “Group by (day, week): “.

quo.confirm(text, default=False, abort=False, prompt_suffix=': ', show_default=True, err=False)
Prompts for confirmation (yes/no question).

If the user aborts the input by sending a interrupt signal this function will catch it and raise a Abort exception.

Changelog
Parameters
text – the question to ask.

default – the default for the prompt.

abort – if this is set to True a negative answer aborts the exception by raising Abort.

prompt_suffix – a suffix that should be added to the prompt.

show_default – shows or hides the default value in the prompt.

err – if set to true the file defaults to stderr instead of stdout, the same as with echo.

quo.progressbar(iterable=None, length=None, label=None, show_eta=True, show_percent=None, show_pos=False, item_show_func=None, fill_char='#', empty_char='-', bar_template='%(label)s [%(bar)s] %(info)s', info_sep=' ', width=36, file=None, color=None)
This function creates an iterable context manager that can be used to iterate over something while showing a progress bar. It will either iterate over the iterable or length items (that are counted up). While iteration happens, this function will print a rendered progress bar to the given file (defaults to stdout) and will attempt to calculate remaining time and more. By default, this progress bar will not be rendered if the file is not a terminal.

The context manager creates the progress bar. When the context manager is entered the progress bar is already created. With every iteration over the progress bar, the iterable passed to the bar is advanced and the bar is updated. When the context manager exits, a newline is printed and the progress bar is finalized on screen.

Note: The progress bar is currently designed for use cases where the total progress can be expected to take at least several seconds. Because of this, the ProgressBar class object won’t display progress that is considered too fast, and progress where the time between steps is less than a second.

No printing must happen or the progress bar will be unintentionally destroyed.

Example usage:

with progressbar(items) as bar:
    for item in bar:
        do_something_with(item)
Alternatively, if no iterable is specified, one can manually update the progress bar through the update() method instead of directly iterating over the progress bar. The update method accepts the number of steps to increment the bar with:

with progressbar(length=chunks.total_bytes) as bar:
    for chunk in chunks:
        process_chunk(chunk)
        bar.update(chunks.bytes)
Changelog
Parameters
iterable – an iterable to iterate over. If not provided the length is required.

length – the number of items to iterate over. By default the progressbar will attempt to ask the iterator about its length, which might or might not work. If an iterable is also provided this parameter can be used to override the length. If an iterable is not provided the progress bar will iterate over a range of that length.

label – the label to show next to the progress bar.

show_eta – enables or disables the estimated time display. This is automatically disabled if the length cannot be determined.

show_percent – enables or disables the percentage display. The default is True if the iterable has a length or False if not.

show_pos – enables or disables the absolute position display. The default is False.

item_show_func – a function called with the current item which can return a string to show the current item next to the progress bar. Note that the current item can be None!

fill_char – the character to use to show the filled part of the progress bar.

empty_char – the character to use to show the non-filled part of the progress bar.

bar_template – the format string to use as template for the bar. The parameters in it are label for the label, bar for the progress bar and info for the info section.

info_sep – the separator between multiple info items (eta etc.)

width – the width of the progress bar in characters, 0 means full terminal width

file – the file to write to. If this is not a terminal then only the label is printed.

color – controls if the terminal supports ANSI colors or not. The default is autodetection. This is only needed if ANSI codes are included anywhere in the progress bar output which is not the case by default.

quo.clear()
Clears the terminal screen. This will have the effect of clearing the whole visible space of the terminal and moving the cursor to the top left. This does not do anything if not connected to a terminal.

Changelog
quo.style(text, fg=None, bg=None, bold=None, dim=None, underline=None, blink=None, reverse=None, reset=True)
Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

Examples:

click.echo(quo.style('Hello World!', fg='green'))
quo.echo(quo.style('ATTENTION!', blink=True))
quo.echo(quo.style('Some things', reverse=True, fg='cyan'))
Supported color names:

black (might be a gray)

red

green

yellow (might be an orange)

blue

magenta

cyan

white (might be light gray)

bright_black

bright_red

bright_green

bright_yellow

bright_blue

bright_magenta

bright_cyan

bright_white

reset (reset the color code only)

New in version 7.0: Added support for bright colors.

Changelog
Parameters
text – the string to style with ansi codes.

fg – if provided this will become the foreground color.

bg – if provided this will become the background color.

bold – if provided this will enable or disable bold mode.

dim – if provided this will enable or disable dim mode. This is badly supported.

underline – if provided this will enable or disable underline.

blink – if provided this will enable or disable blinking.

reverse – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).

reset – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

quo.unstyle(text)
Removes ANSI styling information from a string. Usually it’s not necessary to use this function as quo’s echo function will automatically remove styling if necessary.

Changelog
Parameters
text – the text to remove style information from.

quo.flair(message=None, file=None, nl=True, err=False, color=None, **styles)
This function combines echo() and style() into one call. As such the following two calls are the same:

quo.flair('Hello World!', fg='green')
click.echo(quo.style('Hello World!', fg='green'))
All keyword arguments are forwarded to the underlying functions depending on which one they go with.

Changelog
quo.edit(text=None, editor=None, env=None, require_save=True, extension='.txt', filename=None)
Edits the given text in the defined editor. If an editor is given (should be the full path to the executable but the regular operating system search path is used for finding the executable) it overrides the detected editor. Optionally, some environment variables can be used. If the editor is closed without changes, None is returned. In case a file is edited directly the return value is always None and require_save and extension are ignored.

If the editor cannot be opened a UsageError is raised.

Note for Windows: to simplify cross-platform usage, the newlines are automatically converted from POSIX to Windows and vice versa. As such, the message here will have \n as newline markers.

Parameters
text – the text to edit.

editor – optionally the editor to use. Defaults to automatic detection.

env – environment variables to forward to the editor.

require_save – if this is true, then not saving in the editor will make the return value become None.

extension – the extension to tell the editor about. This defaults to .txt but changing this might change syntax highlighting.

filename – if provided it will edit this file instead of the provided text contents. It will not use a temporary file as an indirection in that case.

quo.launch(url, wait=False, locate=False)
This function launches the given URL (or filename) in the default viewer application for this file type. If this is an executable, it might launch the executable in a new session. The return value is the exit code of the launched application. Usually, 0 indicates success.

Examples:

quo.launch('https://quo.palletsprojects.com/')
quo.launch('/my/downloaded/file', locate=True)
Changelog
Parameters
url – URL or filename of the thing to launch.

wait – waits for the program to stop.

locate – if this is set to True then instead of launching the application associated with the URL it will attempt to launch a file manager with the file located. This might have weird effects if the URL does not point to the filesystem.

quo.getchar(echo=False)
Fetches a single character from the terminal and returns it. This will always return a unicode character and under certain rare circumstances this might return more than one character. The situations which more than one character is returned is when for whatever reason multiple characters end up in the terminal buffer or standard input was not actually a terminal.

Note that this will always read from the terminal, even if something is piped into the standard input.

Note for Windows: in rare cases when typing non-ASCII characters, this function might wait for a second character and then return both at once. This is because certain Unicode characters look like special-key markers.

Changelog
Parameters
echo – if set to True, the character read will also show up on the terminal. The default is to not show it.

quo.pause(info='Press any key to continue ...', err=False)
This command stops execution and waits for the user to press any key to continue. This is similar to the Windows batch “pause” command. If the program is not run through a terminal, this command will instead do nothing.

Changelog
Parameters
info – the info string to print before pausing.

err – if set to message goes to stderr instead of stdout, the same as with echo.

quo.get_terminal_size()
Returns the current size of the terminal as tuple in the form (width, height) in columns and rows.

quo.get_binary_stream(name)
Returns a system stream for byte processing. This essentially returns the stream from the sys module with the given name but it solves some compatibility issues between different Python versions. Primarily this function is necessary for getting binary streams on Python 3.

Parameters
name – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

quo.get_text_stream(name, encoding=None, errors='strict')
Returns a system stream for text processing. This usually returns a wrapped stream around a binary stream returned from get_binary_stream() but it also can take shortcuts on Python 3 for already correctly configured streams.

Parameters
name – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

encoding – overrides the detected default encoding.

errors – overrides the default error mode.

quo.open_file(filename, mode='r', encoding=None, errors='strict', lazy=False, atomic=False)
This is similar to how the File works but for manual usage. Files are opened non lazy by default. This can open regular files as well as stdin/stdout if '-' is passed.

If stdin/stdout is returned the stream is wrapped so that the context manager will not close the stream accidentally. This makes it possible to always use the function like this without having to worry to accidentally close a standard stream:

with open_file(filename) as f:
    ...
Changelog
Parameters
filename – the name of the file to open (or '-' for stdin/stdout).

mode – the mode in which to open the file.

encoding – the encoding to use.

errors – the error handling for this file.

lazy – can be flipped to true to open the file lazily.

atomic – in atomic mode writes go into a temporary file and it’s moved on close.

quo.get_app_dir(app_name, roaming=True, force_posix=False)
Returns the config folder for the application. The default behavior is to return whatever is most appropriate for the operating system.

To give you an idea, for an app called "Foo Bar", something like the following folders could be returned:

Mac OS X:
~/Library/Application Support/Foo Bar

Mac OS X (POSIX):
~/.foo-bar

Unix:
~/.config/foo-bar

Unix (POSIX):
~/.foo-bar

Win XP (roaming):
C:\Documents and Settings\<user>\Local Settings\Application Data\Foo Bar

Win XP (not roaming):
C:\Documents and Settings\<user>\Application Data\Foo Bar

Win 7 (roaming):
C:\Users\<user>\AppData\Roaming\Foo Bar

Win 7 (not roaming):
C:\Users\<user>\AppData\Local\Foo Bar

Changelog
Parameters
app_name – the application name. This should be properly capitalized and can contain whitespace.

roaming – controls if the folder should be roaming or not on Windows. Has no affect otherwise.

force_posix – if this is set to True then on any POSIX system the folder will be stored in the home folder with a leading dot instead of the XDG config home or darwin’s application support folder.

quo.format_filename(filename, shorten=False)
Formats a filename for user display. The main purpose of this function is to ensure that the filename can be displayed at all. This will decode the filename to unicode if necessary in a way that it will not fail. Optionally, it can shorten the filename to not include the full path to the filename.

Parameters
filename – formats a filename for UI display. This will also convert the filename into unicode without failing.

shorten – this optionally shortens the filename to strip of the path that leads up to it.
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
class quo.BaseCommand(name, context_settings=None)
The base command implements the minimal API contract of commands. Most code will never use this as it does not implement a lot of useful functionality but it can act as the direct subclass of alternative parsing methods that do not depend on the quo parser.

For instance, this can be used to bridge quo and other systems like argparse or docopt.

Because base commands do not implement a lot of the API that other parts of quo take for granted, they are not supported for all operations. For instance, they cannot be used with the decorators usually and they have no built-in callback system.

Changelog
Parameters
name – the name of the command to use unless a group overrides it.

context_settings – an optional dictionary with defaults that are passed to the context object.

allow_extra_args = False
the default for the Context.allow_extra_args flag.

allow_interspersed_args = True
the default for the Context.allow_interspersed_args flag.

context_settings = None
an optional dictionary with defaults passed to the context.

ignore_unknown_options = False
the default for the Context.ignore_unknown_options flag.

invoke(ctx)
Given a context, this invokes the command. The default implementation is raising a not implemented error.

main(args=None, prog_name=None, complete_var=None, standalone_mode=True, **extra)
This is the way to invoke a script with all the bells and whistles as a command line application. This will always terminate the application after a call. If this is not wanted, SystemExit needs to be caught.

This method is also available by directly calling the instance of a Command.

Changelog
Parameters
args – the arguments that should be used for parsing. If not provided, sys.argv[1:] is used.

prog_name – the program name that should be used. By default the program name is constructed by taking the file name from sys.argv[0].

complete_var – the environment variable that controls the bash completion support. The default is "_<prog_name>_COMPLETE" with prog_name in uppercase.

standalone_mode – the default behavior is to invoke the script in standalone mode. quo will then handle exceptions and convert them into error messages and the function will never return but shut down the interpreter. If this is set to False they will be propagated to the caller and the return value of this function is the return value of invoke().

extra – extra keyword arguments are forwarded to the context constructor. See Context for more information.

make_context(info_name, args, parent=None, **extra)
This function when given an info name and arguments will kick off the parsing and create a new Context. It does not invoke the actual command callback though.

Parameters
info_name – the info name for this invokation. Generally this is the most descriptive name for the script or command. For the toplevel script it’s usually the name of the script, for commands below it it’s the name of the script.

args – the arguments to parse as list of strings.

parent – the parent context if available.

extra – extra keyword arguments forwarded to the context constructor.

name = None
the name the command thinks it has. Upon registering a command on a Group the group will default the command name with this information. You should instead use the Context’s info_name attribute.

parse_args(ctx, args)
Given a context and a list of arguments this creates the parser and parses the arguments, then modifies the context as necessary. This is automatically invoked by make_context().

class quo.Command(name, context_settings=None, callback=None, params=None, help=None, epilog=None, short_help=None, options_metavar='[OPTIONS]', add_help_option=True, no_args_is_help=False, hidden=False, deprecated=False)
Commands are the basic building block of command line interfaces in quo. A basic command handles command line parsing and might dispatch more parsing to commands nested below it.

Changed in version 7.1: Added the no_args_is_help parameter.

Changelog
Parameters
name – the name of the command to use unless a group overrides it.

context_settings – an optional dictionary with defaults that are passed to the context object.

callback – the callback to invoke. This is optional.

params – the parameters to register with this command. This can be either Option or Argument objects.

help – the help string to use for this command.

epilog – like the help string but it’s printed at the end of the help page after everything else.

short_help – the short help to use for this command. This is shown on the command listing of the parent command.

add_help_option – by default each command registers a --help option. This can be disabled by this parameter.

no_args_is_help – this controls what happens if no arguments are provided. This option is disabled by default. If enabled this will add --help as argument if no arguments are passed

hidden – hide this command from help outputs.

deprecated – issues a message indicating that the command is deprecated.

callback = None
the callback to execute when the command fires. This might be None in which case nothing happens.

collect_usage_pieces(ctx)
Returns all the pieces that go into the usage line and returns it as a list of strings.

format_epilog(ctx, formatter)
Writes the epilog into the formatter if it exists.

format_help(ctx, formatter)
Writes the help into the formatter if it exists.

This is a low-level method called by get_help().

This calls the following methods:

format_usage()

format_help_text()

format_options()

format_epilog()

format_help_text(ctx, formatter)
Writes the help text to the formatter if it exists.

format_options(ctx, formatter)
Writes all the options into the formatter if they exist.

format_usage(ctx, formatter)
Writes the usage line into the formatter.

This is a low-level method called by get_usage().

get_help(ctx)
Formats the help into a string and returns it.

Calls format_help() internally.

get_help_option(ctx)
Returns the help option object.

get_help_option_names(ctx)
Returns the names for the help option.

get_short_help_str(limit=45)
Gets short help for the command or makes it by shortening the long help string.

get_usage(ctx)
Formats the usage line into a string and returns it.

Calls format_usage() internally.

invoke(ctx)
Given a context, this invokes the attached callback (if it exists) in the right way.

make_parser(ctx)
Creates the underlying option parser for this command.

params = None
the list of parameters for this command in the order they should show up in the help page and execute. Eager parameters will automatically be handled before non eager ones.

parse_args(ctx, args)
Given a context and a list of arguments this creates the parser and parses the arguments, then modifies the context as necessary. This is automatically invoked by make_context().

class quo.MultiCommand(name=None, invoke_without_command=False, no_args_is_help=None, subcommand_metavar=None, chain=False, result_callback=None, **attrs)
A multi command is the basic implementation of a command that dispatches to subcommands. The most common version is the Group.

Parameters
invoke_without_command – this controls how the multi command itself is invoked. By default it’s only invoked if a subcommand is provided.

no_args_is_help – this controls what happens if no arguments are provided. This option is enabled by default if invoke_without_command is disabled or disabled if it’s enabled. If enabled this will add --help as argument if no arguments are passed.

subcommand_metavar – the string that is used in the documentation to indicate the subcommand place.

chain – if this is set to True chaining of multiple subcommands is enabled. This restricts the form of commands in that they cannot have optional arguments but it allows multiple commands to be chained together.

result_callback – the result callback to attach to this multi command.

collect_usage_pieces(ctx)
Returns all the pieces that go into the usage line and returns it as a list of strings.

format_commands(ctx, formatter)
Extra format methods for multi methods that adds all the commands after the options.

format_options(ctx, formatter)
Writes all the options into the formatter if they exist.

get_command(ctx, cmd_name)
Given a context and a command name, this returns a Command object if it exists or returns None.

invoke(ctx)
Given a context, this invokes the attached callback (if it exists) in the right way.

list_commands(ctx)
Returns a list of subcommand names in the order they should appear.

parse_args(ctx, args)
Given a context and a list of arguments this creates the parser and parses the arguments, then modifies the context as necessary. This is automatically invoked by make_context().

result_callback = None
The result callback that is stored. This can be set or overridden with the resultcallback() decorator.

resultcallback(replace=False)
Adds a result callback to the chain command. By default if a result callback is already registered this will chain them but this can be disabled with the replace parameter. The result callback is invoked with the return value of the subcommand (or the list of return values from all subcommands if chaining is enabled) as well as the parameters as they would be passed to the main callback.

Example:

@quo.group()
@quo.option('-i', '--input', default=23)
def cli(input):
    return 42

@cli.resultcallback()
def process_result(result, input):
    return result + input
Changelog
Parameters
replace – if set to True an already existing result callback will be removed.

class quo.Group(name=None, commands=None, **attrs)
A group allows a command to have subcommands attached. This is the most common way to implement nesting in quo.

Parameters
commands – a dictionary of commands.

add_command(cmd, name=None)
Registers another Command with this group. If the name is not provided, the name of the command is used.

command(*args, **kwargs)
A shortcut decorator for declaring and attaching a command to the group. This takes the same arguments as command() but immediately registers the created command with this instance by calling into add_command().

commands = None
the registered subcommands by their exported names.

get_command(ctx, cmd_name)
Given a context and a command name, this returns a Command object if it exists or returns None.

group(*args, **kwargs)
A shortcut decorator for declaring and attaching a group to the group. This takes the same arguments as group() but immediately registers the created command with this instance by calling into add_command().

list_commands(ctx)
Returns a list of subcommand names in the order they should appear.

class quo.CommandCollection(name=None, sources=None, **attrs)
A command collection is a multi command that merges multiple multi commands together into one. This is a straightforward implementation that accepts a list of different multi commands as sources and provides all the commands for each of them.

add_source(multi_cmd)
Adds a new multi command to the chain dispatcher.

get_command(ctx, cmd_name)
Given a context and a command name, this returns a Command object if it exists or returns None.

list_commands(ctx)
Returns a list of subcommand names in the order they should appear.

sources = None
The list of registered multi commands.

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
class quo.Parameter(param_decls=None, type=None, required=False, default=None, callback=None, nargs=None, metavar=None, expose_value=True, is_eager=False, envvar=None, autocompletion=None)
A parameter to a command comes in two versions: they are either Options or Arguments. Other subclasses are currently not supported by design as some of the internals for parsing are intentionally not finalized.

Some settings are supported by both options and arguments.

Parameters
param_decls – the parameter declarations for this option or argument. This is a list of flags or argument names.

type – the type that should be used. Either a ParamType or a Python type. The later is converted into the former automatically if supported.

required – controls if this is optional or not.

default – the default value if omitted. This can also be a callable, in which case it’s invoked when the default is needed without any arguments.

callback – a callback that should be executed after the parameter was matched. This is called as fn(ctx, param, value) and needs to return the value.

nargs – the number of arguments to match. If not 1 the return value is a tuple instead of single value. The default for nargs is 1 (except if the type is a tuple, then it’s the arity of the tuple).

metavar – how the value is represented in the help page.

expose_value – if this is True then the value is passed onwards to the command callback and stored on the context, otherwise it’s skipped.

is_eager – eager values are processed before non eager ones. This should not be set for arguments or it will inverse the order of processing.

envvar – a string or list of strings that are environment variables that should be checked.

Changed in version 7.1: Empty environment variables are ignored rather than taking the empty string value. This makes it possible for scripts to clear variables if they can’t unset them.

Changelog
get_default(ctx)
Given a context variable this calculates the default value.

get_error_hint(ctx)
Get a stringified version of the param for use in error messages to indicate which param caused the error.

property human_readable_name
Returns the human readable name of this parameter. This is the same as the name for options, but the metavar for arguments.

process_value(ctx, value)
Given a value and context this runs the logic to convert the value as necessary.

type_cast_value(ctx, value)
Given a value this runs it properly through the type system. This automatically handles things like nargs and multiple as well as composite types.

class quo.Option(param_decls=None, show_default=False, prompt=False, confirmation_prompt=False, hide_input=False, is_flag=None, flag_value=None, multiple=False, count=False, allow_from_autoenv=True, type=None, help=None, hidden=False, show_choices=True, show_envvar=False, **attrs)
Options are usually optional values on the command line and have some extra features that arguments don’t have.

All other parameters are passed onwards to the parameter constructor.

Parameters
show_default – controls if the default value should be shown on the help page. Normally, defaults are not shown. If this value is a string, it shows the string instead of the value. This is particularly useful for dynamic options.

show_envvar – controls if an environment variable should be shown on the help page. Normally, environment variables are not shown.

prompt – if set to True or a non empty string then the user will be prompted for input. If set to True the prompt will be the option name capitalized.

confirmation_prompt – if set then the value will need to be confirmed if it was prompted for.

hide_input – if this is True then the input on the prompt will be hidden from the user. This is useful for password input.

is_flag – forces this option to act as a flag. The default is auto detection.

flag_value – which value should be used for this flag if it’s enabled. This is set to a boolean automatically if the option string contains a slash to mark two options.

multiple – if this is set to True then the argument is accepted multiple times and recorded. This is similar to nargs in how it works but supports arbitrary number of arguments.

count – this flag makes an option increment an integer.

allow_from_autoenv – if this is enabled then the value of this parameter will be pulled from an environment variable in case a prefix is defined on the context.

help – the help string.

hidden – hide this option from help outputs.

class quo.Argument(param_decls, required=None, **attrs)
Arguments are positional parameters to a command. They generally provide fewer features than options but can have infinite nargs and are required by default.

All parameters are passed onwards to the parameter constructor.

.. autoclass:: Parameter
   :members:

.. autoclass:: Option

.. autoclass:: Argument

Context
-------

class quo.Context(command, parent=None, info_name=None, obj=None, auto_envvar_prefix=None, default_map=None, terminal_width=None, max_content_width=None, resilient_parsing=False, allow_extra_args=None, allow_interspersed_args=None, ignore_unknown_options=None, help_option_names=None, token_normalize_func=None, color=None, show_default=None)
The context is a special internal object that holds state relevant for the script execution at every single level. It’s normally invisible to commands unless they opt-in to getting access to it.

The context is useful as it can pass internal objects around and can control special execution features such as reading data from environment variables.

A context can be used as context manager in which case it will call close() on teardown.

New in version 7.1: Added the show_default parameter.

Changelog
Parameters
command – the command class for this context.

parent – the parent context.

info_name – the info name for this invocation. Generally this is the most descriptive name for the script or command. For the toplevel script it is usually the name of the script, for commands below it it’s the name of the script.

obj – an arbitrary object of user data.

auto_envvar_prefix – the prefix to use for automatic environment variables. If this is None then reading from environment variables is disabled. This does not affect manually set environment variables which are always read.

default_map – a dictionary (like object) with default values for parameters.

terminal_width – the width of the terminal. The default is inherit from parent context. If no context defines the terminal width then auto detection will be applied.

max_content_width – the maximum width for content rendered by quo (this currently only affects help pages). This defaults to 80 characters if not overridden. In other words: even if the terminal is larger than that, quo will not format things wider than 80 characters by default. In addition to that, formatters might add some safety mapping on the right.

resilient_parsing – if this flag is enabled then quo will parse without any interactivity or callback invocation. Default values will also be ignored. This is useful for implementing things such as completion support.

allow_extra_args – if this is set to True then extra arguments at the end will not raise an error and will be kept on the context. The default is to inherit from the command.

allow_interspersed_args – if this is set to False then options and arguments cannot be mixed. The default is to inherit from the command.

ignore_unknown_options – instructs quo to ignore options it does not know and keeps them for later processing.

help_option_names – optionally a list of strings that define how the default help parameter is named. The default is ['--help'].

token_normalize_func – an optional function that is used to normalize tokens (options, choices, etc.). This for instance can be used to implement case insensitive behavior.

color – controls if the terminal supports ANSI colors or not. The default is autodetection. This is only needed if ANSI codes are used in texts that quo prints which is by default not the case. This for instance would affect help output.

show_default – if True, shows defaults for all options. Even if an option is later created with show_default=False, this command-level setting overrides it.

abort()
Aborts the script.

allow_extra_args = None
Indicates if the context allows extra args or if it should fail on parsing.

Changelog
allow_interspersed_args = None
Indicates if the context allows mixing of arguments and options or not.

Changelog
args = None
the leftover arguments.

call_on_close(f)
This decorator remembers a function as callback that should be executed when the context tears down. This is most useful to bind resource handling to the script execution. For instance, file objects opened by the File type will register their close callbacks here.

Parameters
f – the function to execute on teardown.

close()
Invokes all close callbacks.

color = None
Controls if styling output is wanted or not.

command = None
the Command for this context.

property command_path
The computed command path. This is used for the usage information on the help page. It’s automatically created by combining the info names of the chain of contexts to the root.

ensure_object(object_type)
Like find_object() but sets the innermost object to a new instance of object_type if it does not exist.

exit(code=0)
Exits the application with a given exit code.

fail(message)
Aborts the execution of the program with a specific error message.

Parameters
message – the error message to fail with.

find_object(object_type)
Finds the closest object of a given type.

find_root()
Finds the outermost context.

forward(**kwargs)
Similar to invoke() but fills in default keyword arguments from the current context if the other command expects it. This cannot invoke callbacks directly, only other commands.

get_help()
Helper method to get formatted help page for the current context and command.

get_usage()
Helper method to get formatted usage string for the current context and command.

help_option_names = None
The names for the help options.

ignore_unknown_options = None
Instructs quo to ignore options that a command does not understand and will store it on the context for later processing. This is primarily useful for situations where you want to call into external programs. Generally this pattern is strongly discouraged because it’s not possibly to losslessly forward all arguments.

Changelog
info_name = None
the descriptive information name

invoke(**kwargs)
Invokes a command callback in exactly the way it expects. There are two ways to invoke this method:

the first argument can be a callback and all other arguments and keyword arguments are forwarded directly to the function.

the first argument is a quo command object. In that case all arguments are forwarded as well but proper quo parameters (options and quo arguments) must be keyword arguments and quo will fill in defaults.

Note that before quo 3.2 keyword arguments were not properly filled in against the intention of this code and no context was created. For more information about this change and why it was done in a bugfix release see Upgrading to 3.2.

invoked_subcommand = None
This flag indicates if a subcommand is going to be executed. A group callback can use this information to figure out if it’s being executed directly or because the execution flow passes onwards to a subcommand. By default it’s None, but it can be the name of the subcommand to execute.

If chaining is enabled this will be set to '*' in case any commands are executed. It is however not possible to figure out which ones. If you require this knowledge you should use a resultcallback().

lookup_default(name)
Looks up the default for a parameter name. This by default looks into the default_map if available.

make_formatter()
Creates the formatter for the help and usage output.

max_content_width = None
The maximum width of formatted content (None implies a sensible default which is 80 for most things).

property meta
This is a dictionary which is shared with all the contexts that are nested. It exists so that quo utilities can store some state here if they need to. It is however the responsibility of that code to manage this dictionary well.

The keys are supposed to be unique dotted strings. For instance module paths are a good choice for it. What is stored in there is irrelevant for the operation of quo. However what is important is that code that places data here adheres to the general semantics of the system.

Example usage:

LANG_KEY = f'{__name__}.lang'

def set_language(value):
    ctx = get_current_context()
    ctx.meta[LANG_KEY] = value

def get_language():
    return get_current_context().meta.get(LANG_KEY, 'en_US')
Changelog
obj = None
the user object stored.

params = None
the parsed parameters except if the value is hidden in which case it’s not remembered.

parent = None
the parent context or None if none exists.

protected_args = None
protected arguments. These are arguments that are prepended to args when certain parsing scenarios are encountered but must be never propagated to another arguments. This is used to implement nested parsing.

resilient_parsing = None
Indicates if resilient parsing is enabled. In that case quo will do its best to not cause any failures and default values will be ignored. Useful for completion.

scope(cleanup=True)
This helper method can be used with the context object to promote it to the current thread local (see get_current_context()). The default behavior of this is to invoke the cleanup functions which can be disabled by setting cleanup to False. The cleanup functions are typically used for things such as closing file handles.

If the cleanup is intended the context object can also be directly used as a context manager.

Example usage:

with ctx.scope():
    assert get_current_context() is ctx
This is equivalent:

with ctx:
    assert get_current_context() is ctx
Changelog
Parameters
cleanup – controls if the cleanup functions should be run or not. The default is to run these functions. In some situations the context only wants to be temporarily pushed in which case this can be disabled. Nested pushes automatically defer the cleanup.

terminal_width = None
The width of the terminal (None is autodetection).

token_normalize_func = None
An optional normalization function for tokens. This is options, choices, commands etc.

quo.get_current_context(silent=False)
Returns the current quo context. This can be used as a way to access the current context object from anywhere. This is a more implicit alternative to the pass_context() decorator. This function is primarily useful for helpers such as echo() which might be interested in changing its behavior based on the current context.

To push the current context, Context.scope() can be used.

Changelog
Parameters
silent – if set to True the return value is None if no context is available. The default behavior is to raise a RuntimeError.

.. autoclass:: Context
   :members:

.. autofunction:: currentcontext

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
exception quo.ClickException(message)
An exception that quo can handle and show to the user.

exception quo.Abort
An internal signalling exception that signals quo to abort.

exception quo.UsageError(message, ctx=None)
An internal exception that signals a usage error. This typically aborts any further handling.

Parameters
message – the error message to display.

ctx – optionally the context that caused this error. quo will fill in the context automatically in some situations.

exception quo.BadParameter(message, ctx=None, param=None, param_hint=None)
An exception that formats out a standardized error message for a bad parameter. This is useful when thrown from a callback or type as quo will attach contextual information to it (for instance, which parameter it is).

Changelog
Parameters
param – the parameter object that caused this error. This can be left out, and quo will attach this info itself if possible.

param_hint – a string that shows up as parameter name. This can be used as alternative to param in cases where custom validation should happen. If it is a string it’s used as such, if it’s a list then each item is quoted and separated.

exception quo.FileError(filename, hint=None)
Raised if a file cannot be opened.

exception quo.NoSuchOption(option_name, message=None, possibilities=None, ctx=None)
Raised if quo attempted to handle an option that does not exist.

Changelog
exception quo.BadOptionUsage(option_name, message, ctx=None)
Raised if an option is generally supplied but the use of the option was incorrect. This is for instance raised if the number of arguments for an option is not correct.

Changelog
Parameters
option_name – the name of the option being used incorrectly.

exception quo.BadArgumentUsage(message, ctx=None)
Raised if an argument is generally supplied but the use of the argument was incorrect. This is for instance raised if the number of values for an argument is not correct.

Changelog

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

class quo.OptionParser(ctx=None)
The option parser is an internal class that is ultimately used to parse options and arguments. It’s modelled after optparse and brings a similar but vastly simplified API. It should generally not be used directly as the high level quo classes wrap it for you.

It’s not nearly as extensible as optparse or argparse as it does not implement features that are implemented on a higher level (such as types or defaults).

Parameters
ctx – optionally the Context where this parser should go with.

add_argument(dest, nargs=1, obj=None)
Adds a positional argument named dest to the parser.

The obj can be used to identify the option in the order list that is returned from the parser.

add_option(opts, dest, action=None, nargs=1, const=None, obj=None)
Adds a new option named dest to the parser. The destination is not inferred (unlike with optparse) and needs to be explicitly provided. Action can be any of store, store_const, append, appnd_const or count.

The obj can be used to identify the option in the order list that is returned from the parser.

allow_interspersed_args = None
This controls how the parser deals with interspersed arguments. If this is set to False, the parser will stop on the first non-option. quo uses this to implement nested subcommands safely.

ctx = None
The Context for this parser. This might be None for some advanced use cases.

ignore_unknown_options = None
This tells the parser how to deal with unknown options. By default it will error out (which is sensible), but there is a second mode where it will ignore it and continue processing after shifting all the unknown options into the resulting args.

parse_args(args)
Parses positional arguments and returns (values, args, order) for the parsed options and arguments as well as the leftover arguments if there are any. The order is a list of objects as they appear on the command line. If arguments appear multiple times they will be memorized multiple times as well.

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


Tests
-------

quo.testing.CliRunner(charset=None, env=None, echo_stdin=False, mix_stderr=True)
The CLI runner provides functionality to invoke a Click command line script for unittesting purposes in a isolated environment. This only works in single-threaded systems without any concurrency as it changes the global interpreter state.

Parameters
charset – the character set for the input and output data. This is UTF-8 by default and should not be changed currently as the reporting to quo only works in Python 2 properly.

env – a dictionary with environment variables for overriding.

echo_stdin – if this is set to True, then reading from stdin writes to stdout. This is useful for showing examples in some circumstances. Note that regular prompts will automatically echo the input.

mix_stderr – if this is set to False, then stdout and stderr are preserved as independent streams. This is useful for Unix-philosophy apps that have predictable stdout and noisy stderr, such that each may be measured independently

get_default_prog_name(cli)
Given a command object it will return the default program name for it. The default is the name attribute or "root" if not set.

invoke(cli, args=None, input=None, env=None, catch_exceptions=True, color=False, **extra)
Invokes a command in an isolated environment. The arguments are forwarded directly to the command line script, the extra keyword arguments are passed to the main() function of the command.

This returns a Result object.

Changelog
Parameters
cli – the command to invoke

args – the arguments to invoke. It may be given as an iterable or a string. When given as string it will be interpreted as a Unix shell command. More details at shlex.split().

input – the input data for sys.stdin.

env – the environment overrides.

catch_exceptions – Whether to catch any other exceptions than SystemExit.

extra – the keyword arguments to pass to main().

color – whether the output should contain color codes. The application can still override this explicitly.

isolated_filesystem()
A context manager that creates a temporary folder and changes the current working directory to it for isolated filesystem tests.

isolation(input=None, env=None, color=False)
A context manager that sets up the isolation for invoking of a command line tool. This sets up stdin with the given input data and os.environ with the overrides from the given dictionary. This also rebinds some internals in quo to be mocked (like the prompt functionality).

This is automatically done in the invoke() method.

Changelog
Parameters
input – the input stream to put into sys.stdin.

env – the environment overrides as dictionary.

color – whether the output should contain color codes. The application can still override this explicitly.

make_env(overrides=None)
Returns the environment overrides for invoking a script.

class quo.testing.Result(runner, stdout_bytes, stderr_bytes, exit_code, exception, exc_info=None)
Holds the captured result of an invoked CLI script.

exc_info = None
The traceback

exception = None
The exception that happened if one did.

exit_code = None
The exit code as integer.

property output
The (standard) output as unicode string.

runner = None
The runner that created the result

property stderr
The standard error as unicode string.

stderr_bytes = None
The standard error as bytes, or None if not available

property stdout
The standard output as unicode string.

stdout_bytes = None
The standard output as bytes
.. currentmodule:: quo.testing

.. autoclass:: CliRunner
   :members:

.. autoclass:: Result
   :members:
