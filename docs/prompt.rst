Prompts
==================

.. currentmodule:: quo

Quo supports prompts in two different places.  The first is automated
prompts when the parameter handling happens, and the second is to ask for
prompts at a later point independently.

This can be accomplished with the :func: `prompt` function, which asks for
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

Input Prompts
-------------

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


Confirmation Prompts
--------------------

To ask if a user wants to continue with an action, the :func:`confirm`
function comes in handy.  By default, it returns the result of the prompt
as a boolean value:

.. code:: python

   from quo import confirm
   
   confirm('Do you want to continue?')
 
