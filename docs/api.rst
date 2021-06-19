API
===

.. module:: quo

This part of the documentation lists the full API reference of all public
classes and functions.

Decorators
----------

quo.command(name=None, cls=None, **attrs)
Creates a new Command and uses the decorated function as callback. This will also automatically attach all decorated option()s and argument()s as parameters to the command.

The name of the command defaults to the name of the function with underscores replaced by dashes. If you want to change that, you can pass the intended name as the first argument.

All keyword arguments are forwarded to the underlying command class.

Once decorated the function turns into a Command instance that can be invoked as a command line utility or be attached to a command Group.

Parameters
name – the name of the command. This defaults to the function name with underscores replaced by dashes.

cls – the command class to instantiate. This defaults to Command.

click.group(name=None, **attrs)
Creates a new Group with a function as callback. This works otherwise the same as command() just that the cls parameter is set to Group.

click.argument(*param_decls, **attrs)
Attaches an argument to the command. All positional arguments are passed as parameter declarations to Argument; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Argument instance manually and attaching it to the Command.params list.

Parameters
cls – the argument class to instantiate. This defaults to Argument.

click.option(*param_decls, **attrs)
Attaches an option to the command. All positional arguments are passed as parameter declarations to Option; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Option instance manually and attaching it to the Command.params list.

Parameters
cls – the option class to instantiate. This defaults to Option.

click.password_option(*param_decls, **attrs)
Shortcut for password prompts.

This is equivalent to decorating a function with option() with the following parameters:

@click.command()
@click.option('--password', prompt=True, confirmation_prompt=True,
              hide_input=True)
def changeadmin(password):
    pass
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

click.pass_context(f)
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

click.echo(message=None, file=None, nl=True, err=False, color=None)
Prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode and binary data that does not fail no matter how badly configured the system is.

Primarily it means that you can print binary data as well as Unicode data on both 2.x and 3.x to the given file in the most appropriate way possible. This is a very carefree function in that it will try its best to not fail. As of Click 6.0 this includes support for unicode output on the Windows console.

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

click.echo_via_pager(text_or_generator, color=None)
This function takes a text and shows it via an environment specific pager on stdout.

Changelog
Parameters
text_or_generator – the text to page, or alternatively, a generator emitting the text to page.

color – controls if the pager supports ANSI colors or not. The default is autodetection.

click.prompt(text, default=None, hide_input=False, confirmation_prompt=False, type=None, value_proc=None, prompt_suffix=': ', show_default=True, err=False, show_choices=True)
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

click.confirm(text, default=False, abort=False, prompt_suffix=': ', show_default=True, err=False)
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

click.progressbar(iterable=None, length=None, label=None, show_eta=True, show_percent=None, show_pos=False, item_show_func=None, fill_char='#', empty_char='-', bar_template='%(label)s [%(bar)s] %(info)s', info_sep=' ', width=36, file=None, color=None)
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

click.clear()
Clears the terminal screen. This will have the effect of clearing the whole visible space of the terminal and moving the cursor to the top left. This does not do anything if not connected to a terminal.

Changelog
click.style(text, fg=None, bg=None, bold=None, dim=None, underline=None, blink=None, reverse=None, reset=True)
Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

Examples:

click.echo(click.style('Hello World!', fg='green'))
click.echo(click.style('ATTENTION!', blink=True))
click.echo(click.style('Some things', reverse=True, fg='cyan'))
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

click.unstyle(text)
Removes ANSI styling information from a string. Usually it’s not necessary to use this function as Click’s echo function will automatically remove styling if necessary.

Changelog
Parameters
text – the text to remove style information from.

click.secho(message=None, file=None, nl=True, err=False, color=None, **styles)
This function combines echo() and style() into one call. As such the following two calls are the same:

click.secho('Hello World!', fg='green')
click.echo(click.style('Hello World!', fg='green'))
All keyword arguments are forwarded to the underlying functions depending on which one they go with.

Changelog
click.edit(text=None, editor=None, env=None, require_save=True, extension='.txt', filename=None)
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

click.launch(url, wait=False, locate=False)
This function launches the given URL (or filename) in the default viewer application for this file type. If this is an executable, it might launch the executable in a new session. The return value is the exit code of the launched application. Usually, 0 indicates success.

Examples:

click.launch('https://click.palletsprojects.com/')
click.launch('/my/downloaded/file', locate=True)
Changelog
Parameters
url – URL or filename of the thing to launch.

wait – waits for the program to stop.

locate – if this is set to True then instead of launching the application associated with the URL it will attempt to launch a file manager with the file located. This might have weird effects if the URL does not point to the filesystem.

click.getchar(echo=False)
Fetches a single character from the terminal and returns it. This will always return a unicode character and under certain rare circumstances this might return more than one character. The situations which more than one character is returned is when for whatever reason multiple characters end up in the terminal buffer or standard input was not actually a terminal.

Note that this will always read from the terminal, even if something is piped into the standard input.

Note for Windows: in rare cases when typing non-ASCII characters, this function might wait for a second character and then return both at once. This is because certain Unicode characters look like special-key markers.

Changelog
Parameters
echo – if set to True, the character read will also show up on the terminal. The default is to not show it.

click.pause(info='Press any key to continue ...', err=False)
This command stops execution and waits for the user to press any key to continue. This is similar to the Windows batch “pause” command. If the program is not run through a terminal, this command will instead do nothing.

Changelog
Parameters
info – the info string to print before pausing.

err – if set to message goes to stderr instead of stdout, the same as with echo.

click.get_terminal_size()
Returns the current size of the terminal as tuple in the form (width, height) in columns and rows.

click.get_binary_stream(name)
Returns a system stream for byte processing. This essentially returns the stream from the sys module with the given name but it solves some compatibility issues between different Python versions. Primarily this function is necessary for getting binary streams on Python 3.

Parameters
name – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

click.get_text_stream(name, encoding=None, errors='strict')
Returns a system stream for text processing. This usually returns a wrapped stream around a binary stream returned from get_binary_stream() but it also can take shortcuts on Python 3 for already correctly configured streams.

Parameters
name – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

encoding – overrides the detected default encoding.

errors – overrides the default error mode.

click.open_file(filename, mode='r', encoding=None, errors='strict', lazy=False, atomic=False)
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

click.get_app_dir(app_name, roaming=True, force_posix=False)
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

click.format_filename(filename, shorten=False)
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

.. autofunction:: currentcontext

.. autoclass:: click.core.ParameterSource
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
