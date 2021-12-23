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

   import quo
   quo.prompt('Please enter a number', default=42.0)



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
   * ``text`` - Plain text or formatted text to be shown before the prompt. This can also be a callable that returns formatted text.
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
    * ``style_transformation`` -
        :class:`~quo.style.StyleTransformation` instance.
    * ``swap_light_and_dark_colors`` - `bool` or
        :class:`~quo.filters.Filter`. When enabled, apply
        :class:`~quo.style.SwapLightAndDarkStyleTransformation`.
        This is useful for switching between dark and light terminal
        backgrounds.
    * ``enable_system_elicit`` - `bool` or
        :class:`~quo.filters.Filter`. Pressing Meta+'!' will show
        a system elicit.
    * ``enable_suspend`` - `bool` or :class:`~quo.filters.Filter`.
        Enable Control-Z style suspension.
    * ``enable_open_in_editor`` - `bool` or
        :class:`~quo.filters.Filter`. Pressing 'v' in Vi mode or
        C-X C-E in emacs mode will open an external editor.
    * ``history`` - :class:`~quo.history.History` instance.
    * ``clipboard`` - :class:`~quo.clipboard.Clipboard` instance.
        (e.g. :class:`~quo.clipboard.InMemoryClipboard`)
    * ``r_elicit`` - Text or formatted text to be displayed on the right side.
        This can also be a callable that returns (formatted) text.
    * ``bottom_toolbar`` - Formatted text or callable which is supposed to
        return formatted text.
    * ``elicit_continuation`` - Text that needs to be displayed for a multiline
        elicit continuation. This can either be formatted text or a callable
        that takes a `elicit_width`, `line_number` and `wrap_count` as input
        and returns formatted text. When this is `None` (the default), then
        `elicit_width` spaces will be used.
    * ``complete_style`` - ``CompleteStyle.COLUMN``,
        ``CompleteStyle.MULTI_COLUMN`` or ``CompleteStyle.READLINE_LIKE``.
    * ``mouse_support`` - `bool` or :class:`~quo.filters.Filter`
        to enable mouse support.
    * ``placeholder`` - Text to be displayed when no input has been given
        yet. Unlike the `default` parameter, this won't be returned as part of
        the output ever. This can be formatted text or a callable that returns
        formatted text.
    * ``refresh_interval`` - (number; in seconds) When given, refresh the UI
        every so many seconds.
    * ``input`` - `Input` object. (Note that the preferred way to change the
        input/output is by creating an `AppSession`.)
    * ``output`` - `Output` object.

Autocompletion

Autocompletion can be added by passing a completer parameter.

.. code:: python

    import quo
     
    session = quo.Prompt()
    suggest = quo.completion.WordCompleter(['<html>', '<body>', '<head>', '<title>'])
    text =  session.prompt('Enter HTML: ', completer=suggest)
    quo.echo(f"You said: {text}")

:class:`~quo.completion.WordCompleter` is a simple completer that
completes the last word before the cursor with any of the given words.

.. image:: ./images/html-completion.png

Confirmation Prompts
--------------------

To ask if a user wants to continue with an action, the :func:`confirm`
function comes in handy.  By default, it returns the result of the prompt
as a boolean value:

.. code:: python

   import quo
   
   quo.confirm('Do you want to continue?')

Syntax highlighting
-------------------

Adding syntax highlighting is as simple as adding a lexer. All of the `Pygments
<http://pygments.org/>`_ lexers can be used after wrapping them in a
:class:`~prompt_toolkit.lexers.PygmentsLexer`. It is also possible to create a
custom lexer by implementing the :class:`~prompt_toolkit.lexers.Lexer` abstract
base class.

.. code:: python

    from pygments.lexers.html import HtmlLexer
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.lexers import PygmentsLexer

    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer))
    print('You said: %s' % text)

.. image:: ../images/html-input.png

The default Pygments colorscheme is included as part of the default style in
prompt_toolkit. If you want to use another Pygments style along with the lexer,
you can do the following:

.. code:: python

    from pygments.lexers.html import HtmlLexer
    from pygments.styles import get_style_by_name
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles.pygments import style_from_pygments_cls

    style = style_from_pygments_cls(get_style_by_name('monokai'))
    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer), style=style,
                  include_default_pygments_style=False)
    print('You said: %s' % text)

We pass ``include_default_pygments_style=False``, because otherwise, both
styles will be merged, possibly giving slightly different colors in the outcome
for cases where where our custom Pygments style doesn't specify a color.

.. _colors:

Colors
------

The colors for syntax highlighting are defined by a
:class:`~prompt_toolkit.styles.Style` instance. By default, a neutral
built-in style is used, but any style instance can be passed to the
:func:`~prompt_toolkit.shortcuts.prompt` function. A simple way to create a
style, is by using the :meth:`~prompt_toolkit.styles.Style.from_dict`
function:

.. code:: python

    from pygments.lexers.html import HtmlLexer
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.lexers import PygmentsLexer

    our_style = Style.from_dict({
        'pygments.comment':   '#888888 bold',
        'pygments.keyword':   '#ff88ff bold',
    })

    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer),
                  style=our_style)


The style dictionary is very similar to the Pygments ``styles`` dictionary,
with a few differences:

- The `roman`, `sans`, `mono` and `border` options are ignored.
- The style has a few additions: ``blink``, ``noblink``, ``reverse`` and ``noreverse``.
- Colors can be in the ``#ff0000`` format, but they can be one of the built-in
  ANSI color names as well. In that case, they map directly to the 16 color
  palette of the terminal.

:ref:`Read more about styling <styling>`.

Coloring the prompt itself
^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to add some colors to the prompt itself. For this, we need to
build some :ref:`formatted text <formatted_text>`. One way of doing this is by
creating a list of style/text tuples. In the following example, we use class
names to refer to the style.

.. code:: python

    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.styles import Style

    style = Style.from_dict({
        # User input (default text).
        '':          '#ff0066',

        # Prompt.
        'username': '#884444',
        'at':       '#00aa00',
        'colon':    '#0000aa',
        'pound':    '#00aa00',
        'host':     '#00ffff bg:#444400',
        'path':     'ansicyan underline',
    })

    message = [
        ('class:username', 'john'),
        ('class:at',       '@'),
        ('class:host',     'localhost'),
        ('class:colon',    ':'),
        ('class:path',     '/user/john'),
        ('class:pound',    '# '),
    ]

    text = prompt(message, style=style)

.. image:: ../images/colored-prompt.png

The `message` can be any kind of formatted text, as discussed :ref:`here
<formatted_text>`. It can also be a callable that returns some formatted text.

By default, colors are taken from the 256 color palette. If you want to have
24bit true color, this is possible by adding the
``color_depth=ColorDepth.TRUE_COLOR`` option to the
:func:`~prompt_toolkit.shortcuts.prompt.prompt` function.

.. code:: python

    from prompt_toolkit.output import ColorDepth

    text = prompt(message, style=style, color_depth=ColorDepth.TRUE_COLOR)


Nested completion
^^^^^^^^^^^^^^^^^

Sometimes you have a command line interface where the completion depends on the
previous words from the input. Examples are the CLIs from routers and switches.
A simple :class:`~prompt_toolkit.completion.WordCompleter` is not enough in
that case. We want to to be able to define completions at multiple hierarchical
levels. :class:`~prompt_toolkit.completion.NestedCompleter` solves this issue:

.. code:: python

    from prompt_toolkit import prompt
    from prompt_toolkit.completion import NestedCompleter

    completer = NestedCompleter.from_nested_dict({
        'show': {
            'version': None,
            'clock': None,
            'ip': {
                'interface': {'brief'}
            }
        },
        'exit': None,
    })

    text = prompt('# ', completer=completer)
    print('You said: %s' % text)

Whenever there is a ``None`` value in the dictionary, it means that there is no
further nested completion at that point. When all values of a dictionary would
be ``None``, it can also be replaced with a set.

Complete while typing
^^^^^^^^^^^^^^^^^^^^^

Autcompletions can be generated automatically while typing or when the user
presses the tab key. This can be configured with the ``complete_while_typing``
option:

.. code:: python

    text = prompt('Enter HTML: ', completer=my_completer,
                  complete_while_typing=True)

Notice that this setting is incompatible with the ``enable_history_search``
option. The reason for this is that the up and down key bindings would conflict
otherwise. So, make sure to disable history search for this.
