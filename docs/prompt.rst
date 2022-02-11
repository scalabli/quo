Prompts
==================

.. currentmodule:: quo

Quo supports prompts in two different places.  The first is automated
prompts when the parameter handling happens, and the second is to ask for
prompts at a later point independently.

This can be accomplished with the :func:`prompt` function, which asks for
valid input according to a type, or the :class:`quo.prompt.Prompt` object, this makes it possible to create a Prompt instance followed by calling prompt() method for every input. This creates a kind of an input session and its packed with lots of features.
You can also use the :func:`quo.confirm` function, which asks for confirmation (yes/no).

The following snippet uses the :func:`quo.prompt` function to ask the user for input
and returns the text. Just like ``input``.

.. code:: python

    from quo import prompt, echo

    text = prompt('Give me some input: ')
    echo(f"You said: {text}")

.. image:: ./images/prompt.png

``App Prompts``
--------------

App prompts are integrated into the app interface.  See
:ref:`app-prompting` for more information.  Internally, it
automatically calls either :func:`quo.prompt` or :func:`quo.confirm` as necessary.

``Input Validation``
----------------------------
A prompt can have a validator attached. To manually ask for user input, you can use the :func:`quo.prompt` function or the :class:`quo.prompt.Prompt` object.
For instance, you can ask for a valid integer:


.. code:: python

   from quo import prompt
   
   prompt('Please enter a valid integer', type=int)

Additionally, the type will be determined automatically if a default value is
provided.  For instance, the following will only accept floats:

.. code:: python

   from quo import prompt

   prompt('Please enter a number', default=42.0)



Parameters
   * ``text`` – the text to show for the prompt.

   * ``default`` *(Optional[str, int])* – The default value to use if no input happens. If this is not given it will prompt until it’s aborted.

   * ``hide`` *(Optional[bool])* – If this is set to true then the input value will be hidden.

   * ``affirm`` – asks for confirmation for the value.

   * ``type`` – the type to use to check the value against.

   * ``value_proc`` – if this parameter is provided it’s a function that is invoked instead of the type conversion to convert a value.

   * ``suffix`` *(Optional[str])* – A suffix that should be added to the prompt.

   * ``show_default`` – shows or hides the default value in the prompt.

   * ``err`` *(Optional[bool])* – If set to true the file defaults to stderr instead of stdout, the same as with echo.

   * ``show_choices`` – Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is “Group by” then the prompt will be “Group by (day, week): “.

Alternatively, you can use class:`quo.types.Validator`
This should implement the :class:`~quo.types.Validator` abstract base class. This requires only one method, named ``validate`` that
takes a :class:`~quo.document.Document` as input and raises
:class:`~quo.errors.ValidationError` when the validation fails.

.. code:: python

    from quo.prompt import Prompt
    from quo.errors import ValidationError
    from quo.types import Validator
    
    session = Prompt()

    class NumberValidator(Validator):
        def validate(self, document):
            text = document.text

            if text and not text.isdigit():
                i = 0

                # Get index of first non numeric character.
                # We want to move the cursor here.
                for i, c in enumerate(text):
                    if not c.isdigit():
                        break

                raise ValidationError(message='This input contains non-numeric characters',
                                      cursor_position=i)

    number = int(session.prompt('Give a number: ', validator=NumberValidator()))
    print(f"You said: {number}")

.. image:: ./images/number-validator.png

By default, the input is validated in real-time while the user is typing, but
Quo can also validate after the user presses the enter key:

.. code:: python

    session.prompt('Give a number: ', validator=NumberValidator(),
           validate_while_typing=False)

If the input validation contains some heavy CPU intensive code, but you don't
want to block the event loop, then it's recommended to wrap the validator class
in a :class:`~quo.validation.ThreadedValidator`.

``Input Prompts using Prompt() class``
-------------------------------------
Input history can be kept between consecutive :class:`quo.prompt.Prompt` calls incase you want to ask for multiple inputs, but each input call needs about the same arguments.

.. code:: python
    
  from quo.prompt import Prompt

  # Create prompt object.
  session = Prompt()

  # Do multiple input calls.
  text1 = session.prompt("What's your name?")
  text2 = session.prompt("Where are you from?")

``Multiline Input``
-------------------
Reading multiline input is as easy as passing the ``multiline=True`` parameter.


.. code:: python

   from quo.prompt import Prompt

   session = Prompt()
   session.prompt('> ', multiline=True)                                                                                               

 
A side effect of this is that the enter key will now insert a newline instead of accepting and returning the input. The user will now have to press :kbd:`Meta+Enter` in order to accept the input. (Or :kbd:`Escape` followed by :kbd:`Enter`.)



It is possible to specify a continuation prompt. This works by passing a
``prompt_continuation`` callable to :func:`~quo.prompt.Prompt.prompt`.
This function is supposed to return :ref:`formatted text <formatted_text>`, or
a list of ``(style, text)`` tuples. The width of the returned text should not
exceed the given width. (The width of the prompt margin is defined by the prompt.)

.. code:: python

    import quo

    session = quo..prompt.Prompt()

    def prompt_continuation(width, line_number, is_soft_wrap):
        return '.' * width
        # Or: return [('', '.' * width)]

    session.prompt('multiline input> ', multiline=True,
           prompt_continuation=prompt_continuation)

.. image:: ../images/multiline-input.png



``Hide Input``
---------------

When the ``hide=True`` flag in :func:`quo.prompt` or ``is_password=True`` flag in :class:`quo.prompt.Prompt` has been given, the input is hidden or replaced by asterisks (``*`` characters) .

``Using function quo.prompt()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

   from quo import prompt

   prompt("Enter password: ", hide=True)

``Using class `quo.prompt.Prompt()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from quo.prompt import Prompt

   session = Prompt()

   session.prompt("Enter password: ", is_password=True)



Parameters
   * ``text`` *(str)*  - Plain text or formatted text to be shown before the prompt. This can also be a callable that returns formatted text.
    * ``wrap_lines`` `bool` or :class:`~quo.filters.Filter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.


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

    * ``refresh_interval`` - (number; in seconds) When given, refresh the UI
        every so many seconds.
    * ``input`` - `Input` object. (Note that the preferred way to change the
        input/output is by creating an `AppSession`.)
    * ``output`` - `Output` object.

Autocompletion
----------------
Autocompletion can be added by passing a completer parameter.

.. code:: python

    import quo
     
    session = quo.prompt.Prompt()
    suggest = quo.completion.WordCompleter(['<html>', '<body>', '<head>', '<title>'])
    text =  session.prompt('Enter HTML: ', completer=suggest)
    quo.echo(f"You said: {text}")

:class:`~quo.completion.WordCompleter` is a simple completer that
completes the last word before the cursor with any of the given words.

.. image:: ./images/html-completion.png

Auto suggestion
---------------

Auto suggestion is a way to propose some input completions to the user like the
`fish shell <http://fishshell.com/>`_.

Usually, the input is compared to the history and when there is another entry
starting with the given text, the completion will be shown as gray text behind
the current input. Pressing the right arrow :kbd:`→` or :kbd:`ctrl-e` will insert
this suggestion, :kbd:`alt-f` will insert the first word of the suggestion.

.. note::

    When suggestions are based on the history, don't forget to share one
    :class:`~quo.history.History` object between consecutive prompt calls. Using a :class:`~quo.prompt.Prompt`

Example:

.. code:: python

    from quo.prompt import Prompt
    from quo.completion import AutoSuggestFromHistory
    from quo.history import InMemoryHistory
    
    session = Prompt()

    while True:
        text = session.prompt('> ', auto_suggest=AutoSuggestFromHistory())
        print(f"You said: {text}")

.. image:: ./images/auto-suggestion.png

A suggestion does not have to come from the history. Any implementation of the
:class:`~quo.completion.AutoSuggest` abstract base class can be
passed as an argument.


Confirmation Prompts
--------------------

To ask if a user wants to continue with an action, the :func:`confirm`
function comes in handy.  By default, it returns the result of the prompt
as a boolean value:
**Parameters**
    - ``text`` *(str)* – the question to ask.

    - ``default`` *(Optional[str, int])* – The default value to use when no input is given. If None, repeat until input is given.

    - ``abort`` *(Optional[bool])* – if this is set to True a negative answer aborts the exception by raising Abort.

    - ``suffix`` *(str)* – a suffix that should be added to the prompt.

    - ``show_default`` *(Optional[bool])* – shows or hides the default value in the prompt.

    - ``err`` *(bool)* – if set to true the file defaults to stderr instead of stdout, the same as with echo.

.. code:: python

   from quo import confirm
   
   confirm('Do you want to continue?')

``Prompt toolbar``
------------------


``Right prompt(rprompt)``
--------------------------
The :class:`quo.prompt.Prompt` class has out of the box support for right prompts as well. People familiar to ZSH could recognise this as the RPROMPT option.

This can be either plain text, formatted text or a callable which returns either.

.. code:: python

   from quo.prompt import Prompt
   from quo.styles import Style

   session = Prompt()
   
   example_style = Style.add({'rprompt': 'bg:green fg:red',})
   
   def get_rprompt():
     return '<rprompt>'

  answer = session.prompt('> ', rprompt=get_rprompt, style=example_style)

.. image:: ./images/rprompt.png

``Syntax highlighting``
-----------------------

Adding syntax highlighting is as simple as adding a lexer. All of the `Pygments
<http://pygments.org/>`_ lexers can be used after wrapping them in a
:class:`~quo.lexers.PygmentsLexer`. It is also possible to create a
custom lexer by implementing the :class:`~quo.lexers.Lexer` abstract
base class.

.. code:: python

    from quo.prompt import Prompt
    from quo.lexers import PygmentsLexer
    from pygments.lexers.html import HtmlLexer
    
    session = Prompt()

    text = session.prompt('Enter HTML: ', lexer=quo.PygmentsLexer(HtmlLexer))
    print(f"You said: {text}")

.. image:: ./images/html-input.png

The default Pygments colorscheme is included as part of the default style in
quo. If you want to use another Pygments style along with the lexer,
you can do the following:

.. code:: python

    import quo
    from pygments.lexers.html import HtmlLexer
    from pygments.styles import get_style_by_name
    from quo.styles.pygments import style_from_pygments_cls

    style = style_from_pygments_cls(get_style_by_name('monokai'))
    session = quo.prompt.Prompt()

    text = session.prompt('Enter HTML: ', lexer=quo.lexers.PygmentsLexer(HtmlLexer), style=style, include_default_pygments_style=False)
    quo.echo(f"You said: {text}")

We pass ``include_default_pygments_style=False``, because otherwise, both
styles will be merged, possibly giving slightly different colors in the outcome
for cases where where our custom Pygments style doesn't specify a color.

``Placeholder text``
--------------------
A placeholer is a text that's displayed as long as no input is given.
This won't be returned as part of the output.
This can be a string, formatted text or a callable that returns formatted text.

Plain text placeholder
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from quo.prompt import Prompt

   session = Prompt(placeholder="..(please type something)")

   session.prompt("What is your name?: ")
 
Formatted text placeholder
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

  from quo.prompt import Prompt
  from quo.text import Text

  session = Prompt(placeholder=Text('<style fg="gray">(please type something)</style>'))
  session.prompt("What is your name?: ")
  

.. _colors:

``Colors``
---------

The colors for syntax highlighting are defined by a
:class:`~quo.styles.Style` instance. By default, a neutral
built-in style is used, but any style instance can be passed to the :class:`~quo.prompt.Prompt` class.

.. note::
      ;func:`quo.prompt` has different semantics and cannot output colored text but :class:`quo.prompt.Prompt` is packed with several ways on how this can be achieved.


A simple way to add color to create a style, is by using the :meth:`~quo.styles.Style.add` function

:ref:`Read more about styling <styling>`.

Coloring the prompt itself
^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to add some colors to the prompt itself. For this, we need to
build some :ref:`formatted text <formatted_text>`. One way of doing this is by
creating a list of style/text tuples. In the following example, we use class names to refer to the style.

.. code:: python
 
    from quo.prompt import Prompt
    from quo.styles import Style

    session = Prompt()

    style = Style.add({
        # User input (default text).
        '':         'fg:blue',

        # Prompt.
        'username': 'fg:red',
        'at':       'fg:white',
        'colon':    'fg:yellow',
        'pound':    'fg:grey',
        'host':     'fg:green bg:#444400',
        'path':     'fg:cyan underline',
    })

    message = [
        ('class:username', 'john'),
        ('class:at',       '@'),
        ('class:host',     'localhost'),
        ('class:colon',    ':'),
        ('class:path',     '/user/john'),
        ('class:pound',    '# '),
    ]

    text = session.prompt(message, style=style)

.. image:: ./images/colored-prompt.png

The `message` can be any kind of formatted text, as discussed :ref:`here
<formatted_text>`. It can also be a callable that returns some formatted text.

By default, colors are taken from the 256 color palette. If you want to have 24bit true color, this is possible by adding the ``color_depth=ColorDepth.TRUE_COLOR`` option to the :func:`~quo.prompt.Prompt.prompt` function.

.. code:: python

    from quo.prompt import Prompt
    from quo.color import ColorDepth

    session = Prompt()

    text = session.prompt(message, style=style, color_depth=ColorDepth.TRUE_COLOR)


Nested completion
^^^^^^^^^^^^^^^^^

Sometimes you have a command line interface where the completion depends on the
previous words from the input. Examples are the CLIs from routers and switches.
A simple :class:`~quo.completion.WordCompleter` is not enough in that case. We want to to be able to define completions at multiple hierarchical levels. :class:`~quo.completion.NestedCompleter` solves this issue:

.. code:: python

    from quo.prompt import Prompt
    from quo.completion import NestedCompleter

    session = Prompt()
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

    text = session.prompt('# ', completer=completer)
    print('You said: %s' % text)

Whenever there is a ``None`` value in the dictionary, it means that there is no further nested completion at that point. When all values of a dictionary would be ``None``, it can also be replaced with a set.

Complete while typing
^^^^^^^^^^^^^^^^^^^^^

Autcompletions can be generated automatically while typing or when the user presses the tab key. This can be configured with the ``complete_while_typing`` option:

.. code:: python

    text = session.prompt('Enter HTML: ', completer=my_completer, complete_while_typing=True)

Notice that this setting is incompatible with the ``enable_history_search``
option. The reason for this is that the up and down key bindings would conflict
otherwise. So, make sure to disable history search for this.


History
-------

A :class:`~quo.history.History` object keeps track of all the previously entered strings, so that the up-arrow can reveal previously entered items.

The recommended way is to use a :class:`~quo.prompt.Prompt`, which uses an :class:`~quo.history.InMemoryHistory` for the entire session by default. The following example has a history out of the box:

.. code:: python

   from quo.prompt import Prompt

   session = Prompt()

   while True:
       session.prompt()

To persist a history to disk, use a :class:`~quo.history.FileHistory` instead of the default :class:`~quo.history.InMemoryHistory`. This history object can be
passed either to a :class:`~quo.prompt.Prompt`.
For instance:

.. code:: python

   from quo.prompt import Prompt
   from quo.history import FileHistory

   session = Prompt(history=FileHistory('~/.myhistory'))

   while True:
       session.prompt()

Adding a bottom toolbar
-----------------------

Adding a bottom toolbar is as easy as passing a ``bottom_toolbar`` argument to :func:`~quo.prompt.Prompt.prompt`. This argument be either plain text, :ref:`formatted text <formatted_text>` or a callable that returns plain or formatted text.

When a function is given, it will be called every time the prompt is rendered,
so the bottom toolbar can be used to display dynamic information.

The toolbar is always erased when the prompt returns.
Here we have an example of a callable that returns an
:class:`~quo.text.HTML` object. By default, the toolbar
has the **reversed style**, which is why we are setting the background instead of the foreground.

.. code:: python

    from quo.prompt import Prompt
    from quo.text import HTML

    session = Prompt()

    def bottom_toolbar():
        return HTML('This is a <b><style bg="red">Toolbar</style></b>!')
    # Returns a callable
    text = session.prompt('> ', bottom_toolbar=bottom_toolbar)

.. image:: ./images/bottom-toolbar.png

Similar, we could use a list of style/text tuples.

.. code:: python

    from quo.prompt import Prompt
    from quo.styles import Style

    session = Prompt()

    def bottom_toolbar():
        return [('class:bottom-toolbar', ' This is a toolbar. ')]

    style = Style.add({
        'bottom-toolbar': 'fg:white bg:green',
    })

    text = session.prompt('> ', bottom_toolbar=bottom_toolbar, style=style)
    print(f'You said: {text}')

The default class name is ``bottom-toolbar`` and that will also be used to fill the background of the toolbar.


Adding custom key bindings
--------------------------

By default, every prompt already has a set of key bindings which implements the usual Vi or Emacs behaviour. We can extend this by passing another
:class:`~quo.keys.KeyBinder` instance to the ``bind`` argument of the :class:`~quo.prompt.Prompt` class.

.. note::
    :func:`quo.prompt` function does not support key bindings but :class:`quo.prompt.Prompt` does


An example of a prompt that prints ``'hello world'`` when :kbd:`Control-T` is pressed.

.. code:: python

    from quo.prompt import Prompt
    from quo.keys import KeyBinder

    kb = KeyBinder()
    session = Prompt()

    @kb.add('ctrl-t')
    def _(event):
    # Say 'hello' when `ctrl-t` is pressed."
        print("Hello, World!")

    @kb.add('ctrl-x')
    def _(event):
      #Exit when `ctrl-x` is pressed. "
        event.app.exit()

    text = session.prompt('> ', bind=kb)

Enable key bindings according to a condition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often, some key bindings can be enabled or disabled according to a certain
condition. For instance, the Emacs and Vi bindings will never be active at the
same time, but it is possible to switch between Emacs and Vi bindings at run
time.

In order to enable a key binding according to a certain condition, we have to
pass it a :class:`~quo.filters.Condition` instance. (:ref:`Read more about filters <filters>`.)

.. code:: python

    import datetime
    from quo.prompt import Prompt
    from quo.keys import KeyBinder
    from quo.filters import Condition

    kb = KeyBinder()
    session = Prompt()

    @Condition
    def second_half():
        " Only activate key binding on the second half of each minute. "
        return datetime.datetime.now().second > 30

    @kb.add('ctrl-t', filter=second_half)
    def _(event):
        # ...
        pass

    session.prompt('> ', bind=kb)

Using control-space for completion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An popular short cut that people sometimes use it to use control-space for
opening the autocompletion menu instead of the tab key. This can be done with the following key binding.

.. code:: python

    from quo.keys import KeyBinder

    kb = KeyBinder()

    @kb.add('ctrl-space')
    def _(event):
        " Initialize autocompletion, or select the next completion. "
        buff = event.app.current_buffer
        if buff.complete_state:
            buff.complete_next()
        else:
            buff.start_completion(select_first=False)


Other Prompt options
--------------------

Multiline input
^^^^^^^^^^^^^^^

Reading multiline input is as easy as passing the ``multiline=True`` parameter.

.. code:: python

    import quo

    session = quo.Prompt()
    session.prompt('> ', multiline=True)

A side effect of this is that the enter key will now insert a newline instead
of accepting and returning the input. The user will now have to press
:kbd:`Meta+Enter` in order to accept the input. (Or :kbd:`Escape` followed by
:kbd:`Enter`.)

It is possible to specify a continuation prompt. This works by passing a
``prompt_continuation`` callable to :func:`~prompt_toolkit.shortcuts.prompt`.
This function is supposed to return :ref:`formatted text <formatted_text>`, or
a list of ``(style, text)`` tuples. The width of the returned text should not
exceed the given width. (The width of the prompt margin is defined by the
prompt.)

.. code:: python

    import quo

    session = quo.Prompt()

    def prompt_continuation(width, line_number, is_soft_wrap):
        return '.' * width
        # Or: return [('', '.' * width)]

    session.prompt('multiline input> ', multiline=True,
           prompt_continuation=prompt_continuation)

.. image:: ../images/multiline-input.png

Mouse support
^^^^^^^^^^^^^

There is limited mouse support for positioning the cursor, for scrolling (in case of large multiline inputs) and for clicking in the autocompletion menu.

Enabling can be done by passing the ``mouse_support=True`` option.

.. code:: python

    from quo.prompt import Prompt

    session = Prompt()
    session.prompt('What is your name: ', mouse_support=True)


Line wrapping
^^^^^^^^^^^^^

Line wrapping is enabled by default. This is what most people are used to and this is what GNU Readline does. When it is disabled, the input string will scroll horizontally.

.. code:: python

    from quo.prompt import Prompt

    session = Prompt()
    session.prompt('What is your name: ', wrap_lines=False)
