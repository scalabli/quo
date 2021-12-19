Prompts
==================

.. currentmodule:: quo

Quo supports prompts in two different places.  The first is automated
prompts when the parameter handling happens, and the second is to ask for
prompts at a later point independently.

This can be accomplished with the :func:`prompt` function, which asks for
valid input according to a type, or the :func:`Prompt` object, this makes it possible to create a Prompt instance followed by calling prompt() method for every input. This creates a kind of an input session and its packed with lots of features.
You can also use the :func:`confirm` function, which asks
for confirmation (yes/no).

The following snippet uses the :func:`prompt` function to ask the user for input
and returns the text. Just like ``input``.

.. code:: python

    import quo

    text = quo.prompt('Give me some input: ')
    quo.echo(f"You said: {text}")

.. image:: ./images/prompt.png

App Prompts
--------------

App prompts are integrated into the app interface.  See
:ref:`app-prompting` for more information.  Internally, it
automatically calls either :func:`prompt` or :func:`confirm` as necessary.

Input Prompts using prompt() function
--------------------------------------

To manually ask for user input, you can use the :func:`prompt` function.
By default, it accepts any Unicode string, but you can ask for any other
type.  For instance, you can ask for a valid integer:

.. code:: python

   import quo
   
   quo.prompt('Please enter a valid integer', type=int)

Additionally, the type will be determined automatically if a default value is
provided.  For instance, the following will only accept floats:

.. code:: python

   from quo import prompt
   prompt('Please enter a number', default=42.0)



Parameters
   * ``text`` – the text to show for the prompt.

   * ``default`` – the default value to use if no input happens. If this is not given it will prompt until it’s aborted.

   * ``hide`` – if this is set to true then the input value will be hidden.

   * ``affirm`` – asks for confirmation for the value.

   * ``type`` – the type to use to check the value against.

   * ``value_proc`` – if this parameter is provided it’s a function that is invoked instead of the type conversion to convert a value.

   * ``suffix`` – a suffix that should be added to the prompt.

   * ``show_default`` – shows or hides the default value in the prompt.

   * ``err`` – if set to true the file defaults to stderr instead of stdout, the same as with echo.

   * ``show_choices`` – Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is “Group by” then the prompt will be “Group by (day, week): “.

Input Prompts using Prompt() object
-------------------------------------
Input history can be kept between consecutive Prompt() calls incase you want to ask for multiple inputs, but each input call needs about the same arguments.

.. code:: python
    
  import quo

  # Create prompt object.
  session = quo.Prompt()

  # Do multiple input calls.
  text1 = session.prompt("What's your name?")
  text2 = session.prompt("Where are you from?")

Parameters
   * ``message`` - Plain text or formatted text to be shown before the prompt. This can also be a callable that returns formatted text.
   * ``multiline`` - `bool` or :class:`~quo.filters.Filter`.
        When True, prefer a layout that is more adapted for multiline input.
        Text after newlines is automatically indented, and search/arg input is
        shown below the input, instead of replacing the elicit.
    * ``wrap_lines`` `bool` or :class:`~quo.filters.Filter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.
    * ``is_password`` - Show asterisks instead of the actual typed characters.
    * ``editing_mode`` - ``EditingMode.VI`` or ``EditingMode.EMACS``.
    * ``vi_mode`` - `bool`, if True, Identical to ``editing_mode=EditingMode.VI``.
    * ``complete_while_typing`` - `bool` or
        :class:`~quo.filters.Filter`. Enable autocompletion while
        typing.
    * ``validate_while_typing`` - `bool` or
        :class:`~quo.filters.Filter`. Enable input validation while
        typing.
    * ``enable_history_search`` - `bool` or
        :class:`~quo.filters.Filter`. Enable up-arrow parting
        string matching.
    * ``search_ignore_case`` - 
        :class:`~quo.filters.Filter`. Search case insensitive.
    * ``lexer`` - :class:`~quo.lexers.Lexer` to be used for the
        syntax highlighting.
    * ``validator`` - :class:`~quo.validation.Validator` instance
        for input validation.
    * ``completer`` - :class:`~quo.completion.Completer` instance
        for input completion.
    * ``complete_in_thread`` - `bool` or
        :class:`~quo.filters.Filter`. Run the completer code in a
        background thread in order to avoid blocking the user interface.
        For ``CompleteStyle.READLINE_LIKE``, this setting has no effect. There
        we always run the completions in the main thread.
    * ``reserve_space_for_menu`` - Space to be reserved for displaying the menu.
        (0 means that no space needs to be reserved.)
    * ``auto_suggest`` - :class:`~quo.auto_suggest.AutoSuggest`
        instance for input suggestions.
    * ``style`` - :class:`.Style` instance for the color scheme.
    * ``include_default_pygments_style`` - `bool` or
        :class:`~quo.filters.Filter`. Tell whether the default
        styling for Pygments lexers has to be included. By default, this is
        true, but it is recommended to be disabled if another Pygments style is
        passed as the `style` argument, otherwise, two Pygments styles will be
        merged.
    :param style_transformation:
        :class:`~quo.style.StyleTransformation` instance.
    :param swap_light_and_dark_colors: `bool` or
        :class:`~quo.filters.Filter`. When enabled, apply
        :class:`~quo.style.SwapLightAndDarkStyleTransformation`.
        This is useful for switching between dark and light terminal
        backgrounds.
param enable_system_elicit: `bool` or
        :class:`~quo.filters.Filter`. Pressing Meta+'!' will show
        a system elicit.
    :param enable_suspend: `bool` or :class:`~quo.filters.Filter`.
        Enable Control-Z style suspension.
    :param enable_open_in_editor: `bool` or
        :class:`~quo.filters.Filter`. Pressing 'v' in Vi mode or
        C-X C-E in emacs mode will open an external editor.
    :param history: :class:`~quo.history.History` instance.
    :param clipboard: :class:`~quo.clipboard.Clipboard` instance.
        (e.g. :class:`~quo.clipboard.InMemoryClipboard`)
    :param r_elicit: Text or formatted text to be displayed on the right side.
        This can also be a callable that returns (formatted) text.
    :param bottom_toolbar: Formatted text or callable which is supposed to
        return formatted text.
    :param elicit_continuation: Text that needs to be displayed for a multiline
        elicit continuation. This can either be formatted text or a callable
        that takes a `elicit_width`, `line_number` and `wrap_count` as input
        and returns formatted text. When this is `None` (the default), then
        `elicit_width` spaces will be used.
    :param complete_style: ``CompleteStyle.COLUMN``,
        ``CompleteStyle.MULTI_COLUMN`` or ``CompleteStyle.READLINE_LIKE``.
    :param mouse_support: `bool` or :class:`~quo.filters.Filter`
        to enable mouse support.
    :param placeholder: Text to be displayed when no input has been given
        yet. Unlike the `default` parameter, this won't be returned as part of
        the output ever. This can be formatted text or a callable that returns
        formatted text.
    :param refresh_interval: (number; in seconds) When given, refresh the UI
        every so many seconds.
    :param input: `Input` object. (Note that the preferred way to change the
        input/output is by creating an `AppSession`.)
    :param output: `Output` object.
Confirmation Prompts
--------------------

To ask if a user wants to continue with an action, the :func:`confirm`
function comes in handy.  By default, it returns the result of the prompt
as a boolean value:

.. code:: python

   from quo import confirm
   
   confirm('Do you want to continue?')
 
