.. _kb:

Key binding 🗝️
===============
A key binding is an association between a physical key on a keyboard and a parameter. A parameter can have any number of key bindings associated with it, and a particular key binding can control any number of parameters.

.. note::

  This page contains a couple of extra notes about key bindings.

Key bindings can be defined by creating a
:class:`~quo.keys.KeyBinder` instance:


.. code:: python

    from quo.keys import KeyBinder

    kb = KeyBinder()

    @kb.add('a')
    def _(start):
        " Do something if 'a' has been pressed. "
        ...


    @kb.add('ctrl-t')
    def _(event):
        " Do something if Control-T has been pressed. "
        ...

.. note::

    :kbd:`ctrl-q` (control-q) and :kbd:`ctrl-s` (control-s) are often captured by the
    terminal, because they were used traditionally for software flow control.
    When this is enabled, the application will automatically freeze when
    :kbd:`ctrl-s` is pressed, until :kbd:`ctrl-q` is pressed. It won't be possible to
    bind these keys.

    In order to disable this, execute the following command in your shell, or even
    add it to your `.bashrc`.

    .. code::

        stty -ixon

Key bindings can even consist of a sequence of multiple keys. The binding is only triggered when all the keys in this sequence are pressed.

.. code:: python

    @kb.add('q', 'u', 'o')
    def _(start):
        " Do something if 'a' is pressed and then 'b' is pressed. "
        ...

If the user presses only `q`, then nothing will happen until either a second
key (like `u` or `o`) has been pressed or until the timeout expires.


``List of special keys``
-------------------------

Besides literal characters, any of the following keys can be used in a key
binding:

+-------------------+--------------------------------------------------+
| Name              + Possible keys                                    |
+===================+==================================================+
| Escape            | :kbd:`escape`                                    |
| Shift + escape    | :kbd:`s-escape`                                  |
+-------------------+--------------------------------------------------+
| Arrows            | :kbd:`left`,                                     |
|                   | :kbd:`right`,                                    |
|                   | :kbd:`up`,                                       |
|                   | :kbd:`down`                                      |
+-------------------+--------------------------------------------------+
| Navigation        | :kbd:`home`,                                     |
|                   | :kbd:`end`,                                      |
|                   | :kbd:`delete`,                                   |
|                   | :kbd:`pageup`,                                   |
|                   | :kbd:`pagedown`,                                 |
|                   | :kbd:`insert`                                    |
+-------------------+--------------------------------------------------+
| Control+letter    | :kbd:`ctrl-a`, :kbd:`ctrl-b`, :kbd:`ctrl-c`,     |
|                   | :kbd:`ctrl-d`, :kbd:`ctrl-e`, :kbd:`ctrl-f`,     |
|                   | :kbd:`ctrl-g`, :kbd:`ctrl-h`, :kbd:`cttl-i`,     |
|                   | :kbd:`ctrl-j`, :kbd:`ctrl-k`, :kbd:`ctrl-l`,     |
|                   |                                                  |
|                   | :kbd:`ctrl-m`, :kbd:`ctrl-n`, :kbd:`ctrl-o`,     |
|                   | :kbd:`ctrl-p`, :kbd:`ctrl-q`, :kbd:`ctrl-r`,     |
|                   | :kbd:`ctrl-s`, :kbd:`ctrl-t`, :kbd:`ctrl-u`,     |
|                   | :kbd:`ctrl-v`, :kbd:`ctrl-w`, :kbd:`ctrl-x`,     |
|                   |                                                  |
|                   | :kbd:`ctrl-y`, :kbd:`ctrl-z`                     |
+-------------------+--------------------------------------------------+
| Control + number  | :kbd:`ctrl-1`, :kbd:`ctrl-2`, :kbd:`ctrl-3`,     |
|                   | :kbd:`ctrl-4`, :kbd:`ctrl-5`, :kbd:`ctrl-6`,     |
|                   | :kbd:`ctrl-7`, :kbd:`ctrl-8`, :kbd:`ctrl-9`,     |
|                   | :kbd:`ctrl-0`                                    |
+-------------------+--------------------------------------------------+
| Control + arrow   | :kbd:`ctrl-left`,                                |
|                   | :kbd:`ctrl-right`,                               |
|                   | :kbd:`ctrl-up`,                                  |
|                   | :kbd:`ctrl-down`                                 |
+-------------------+--------------------------------------------------+
| Other control     | :kbd:`ctrl-@`,                                   |
| keys              | :kbd:`ctrl-\\`,                                  |
|                   | :kbd:`ctrl-]`,                                   |
|                   | :kbd:`ctrl-^`,                                   |
|                   | :kbd:`ctrl-_`,                                   |
|                   | :kbd:`ctrl-delete`                               |
+-------------------+--------------------------------------------------+
| Shift + arrow     | :kbd:`s-left`,                                   |
|                   | :kbd:`s-right`,                                  |
|                   | :kbd:`s-up`,                                     |
|                   | :kbd:`s-down`                                    |
+-------------------+--------------------------------------------------+
| Control + Shift + | :kbd:`c-s-left`,                                 |
| arrow             | :kbd:`c-s-right`,                                |
|                   | :kbd:`c-s-up`,                                   |
|                   | :kbd:`c-s-down`                                  |
+-------------------+--------------------------------------------------+
| Other shift       | :kbd:`s-delete`,                                 |
| keys              | :kbd:`s-tab`                                     |
+-------------------+--------------------------------------------------+
| F-keys            | :kbd:`f1`, :kbd:`f2`, :kbd:`f3`,                 |
|                   | :kbd:`f4`, :kbd:`f5`, :kbd:`f6`,                 |
|                   | :kbd:`f7`, :kbd:`f8`, :kbd:`f9`,                 |
|                   | :kbd:`f10`, :kbd:`f11`, :kbd:`f12`,              |
|                   |                                                  |
|                   | :kbd:`f13`, :kbd:`f14`, :kbd:`f15`,              |
|                   | :kbd:`f16`, :kbd:`f17`, :kbd:`f18`,              |
|                   | :kbd:`f19`, :kbd:`f20`, :kbd:`f21`,              |
|                   | :kbd:`f22`, :kbd:`f23`, :kbd:`f24`               |
+-------------------+--------------------------------------------------+

There are a couple of useful aliases as well:

+-------------------+-------------------+-----+
| :kbd:`ctrl-h`        | :kbd:`backspace`     |
+-------------------+-------------------+-----+
| :kbd:`ctrl-@`        | :kbd:`ctrl-space`    |
+-------------------+-------------------+-----+
| :kbd:`ctrl-m`        | :kbd:`enter`         |
+-------------------+-------------------+-----+
| :kbd:`ctrl-i`        | :kbd:`tab`           |
+-------------------+-------------------+-----+

.. note::

    Note that the supported keys are limited to what typical VT100 terminals
    offer. Binding :kbd:`ctrl-7` (control + number 7) for instance is not
    supported.


``Binding alt+something, option+something or meta+something``
---------------------------------------------------------------

Vt100 terminals translate the alt key into a leading :kbd:`escape` key.
For instance, in order to handle :kbd:`alt-f`, we have to handle
:kbd:`escape` + :kbd:`f`. Notice that we receive this as two individual keys.
This means that it's exactly the same as first typing :kbd:`escape` and then
typing :kbd:`f`. Something this alt-key is also known as option or meta.

In code that looks as follows:

.. code:: python

    @kb.add('escape', 'f')
    def _(event):
        " Do something if alt-f or meta-f have been pressed. "


``Wildcards``
-------------

Sometimes you want to catch any key that follows after a certain key stroke.
This is possible by binding the '<any>' key:

.. code:: python

    @bindings.add('a', '<any>')
    def _(start):
        ...

This will handle `aa`, `ab`, `ac`, etcetera. The key binding can check the
`event` object for which keys exactly have been pressed.


``Attaching a Condition to key bindings``
---------------------------------------

In order to enable a key binding according to a certain condition, we have to
pass it to :class:`~quo.Condition` instance. (:ref:`Read more about filters <filters>`.)

.. code:: python

    import datetime
    from quo import Condition

    @Condition
    def is_active():
        " Only activate key binding on the second half of each minute. "
        return datetime.datetime.now().second > 30

    @kb.add('ctrl-t', filter=is_active)
    def _(event):
        # ...
        pass

The key binding will be ignored when this condition is not satisfied.


``ConditionalKeyBindings: Disabling a set of key bindings``
-------------------------------------------------------------

Sometimes you want to enable or disable a whole set of key bindings according
to a certain condition. This is possible by wrapping it in a
:class:`~quo.keys.ConditionalKeyBindings` object.

.. code:: python

    from quo import Condition

    @Condition
    def is_active():
        " Only activate key binding on the second half of each minute. "
        return datetime.datetime.now().second > 30

     bindings = quo.keys.ConditionalKeyBindings(
         bind=my_bindings,
         filter=is_active)

If the condition is not satisfied, all the key bindings in `my_bindings` above
will be ignored.


``Merging key bindings``
-------------------------

Sometimes you have different parts of your application generate a collection of
key bindings. It is possible to merge them together through the
:func:`~quo.keys.merge_key_bindings` function. This is preferred above passing a :class:`~quo.keys.KeyBinder` object around and having everyone populate it.

.. code:: python

    from quo.keys import merge_key_bindings

    bindings = merge_key_bindings([
        bindings1,
        bindings2,
    ])


``Eager``
----------

Usually not required, but if ever you have to override an existing key binding,
the `eager` flag can be useful.

Suppose that there is already an active binding for `ab` and you'd like to add
a second binding that only handles `a`. When the user presses only `a`,
quo  has to wait for the next key press in order to know which
handler to call.

By passing the `eager` flag to this second binding, we are actually saying that quo shouldn't wait for longer matches when all the keys in this key binding are matched. So, if `a` has been pressed, this second binding will be called, even if there's an active `ab` binding.

.. code:: python

    @kb.add('a', 'b')
    def binding_1(event):
        ...

    @kb.add('a', eager=True)
    def binding_2(event):
        ...

This is mainly useful in order to conditionally override another binding.

``Asyncio coroutines``
-------------------------

Key binders handlers can be asyncio coroutines.

.. code:: python


    @kb.add('x')
    async def print_hello(event):
        """
        Pressing 'x' will print 5 times "hello" in the background above the
        prompt.
        """
        for i in range(5):
            # Print hello above the current prompt.
            print("Hello")

            # Sleep, but allow further input editing in the meantime.
            await asyncio.sleep(1)

If the user accepts the input on the prompt, while this coroutine is not yet
finished , an `asyncio.CancelledError` exception will be thrown in this
coroutine.


``Timeouts``
---------------

There are two timeout settings that effect the handling of keys.

- ``Application.ttimeoutlen``: Like Vim's `ttimeoutlen` option.
  When to flush the input (For flushing escape keys.) This is important on
  terminals that use vt100 input. We can't distinguish the escape key from for
  instance the left-arrow key, if we don't know what follows after "\x1b". This
  little timer will consider "\x1b" to be escape if nothing did follow in this
  time span.  This seems to work like the `ttimeoutlen` option in Vim.

- ``KeyProcessor.timeoutlen``: like Vim's `timeoutlen` option.
  This can be `None` or a float.  For instance, suppose that we have a key
  binding AB and a second key binding A. If the uses presses A and then waits,
  we don't handle this binding yet (unless it was marked 'eager'), because we
  don't know what will follow. This timeout is the maximum amount of time that
  we wait until we call the handlers anyway. Pass `None` to disable this
  timeout.


``Recording macros``
----------------------

Both Emacs and Vi mode allow macro recording. By default, all key presses are
recorded during a macro, but it is possible to exclude certain keys by setting
the `record_in_macro` parameter to `False`:

.. code:: python

    @kb.add('ctrl-t', record_in_macro=False)
    def _(event):
        # ...
        pass


``Creating new Vi text objects and operators``
------------------------------------------------

We tried very hard to ship prompt_toolkit with as many as possible Vi text
objects and operators, so that text editing feels as natural as possible to Vi
users.

If you wish to create a new text object or key binding, that is actually
possible. Check the `custom-vi-operator-and-text-object.py` example for more
information.


Processing `.inputrc`
---------------------

GNU readline can be configured using an `.inputrc` configuration file. This file
contains key bindings as well as certain settings. Right now, quo
doesn't support `.inputrc`, but it should be possible in the future.
