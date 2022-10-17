Utilities
===============


``Screen Clearing``
--------------------
To clear the terminal screen, you can use the :func:`quo.clear` function. It does what the name suggests: it clears the entire visible screen in a platform-agnostic way:

.. code:: python

    from quo import clear

    clear()


``Getting Characters from Terminal(getchar)``
----------------------------------------------

Normally, when reading input from the terminal, you would read from
standard input.  However, this is buffered input and will not show up until
the line has been terminated.  In certain circumstances, you might not want
to do that and instead read individual characters as they are being written.

For this, Quo provides the :func:`getchar` function which reads a single
character from the terminal buffer and returns it as a Unicode character.

Note that this function will always read from the terminal, even if stdin
is instead a pipe.

.. code:: python

    from quo import getchar
    
    gc = getchar()

    if gc == 'y':
        print('We will go on')
    elif gc == 'n':
        print('Abort!')
 

Note that this reads raw input, which means that things like arrow keys
will show up in the platform's native escape format.  The only characters
translated are ``^C`` and ``^D`` which are converted into keyboard
interrupts and end of file exceptions respectively.  This is done because
otherwise, it's too easy to forget about that and to create scripts that
cannot be properly exited.

``Exitting``
------------
Quo has a low-level exit that skips Python's cleanup and speeds up exit by about 10ms for things like shell completion.
**Parmameters**
     - ``code`` *(str)* - Exit code.

.. code:: python

 from quo import exit

 exit(1)



``Waiting for Key Press(pause)``
--------------------------------

Sometimes, it's useful to pause until the user presses any key on the
keyboard.

In quo, this can be accomplished with the :func:`quo.pause` function.  This
function will print a quick message to the terminal (which can be
customized) and wait for the user to press a key.  In addition to that,
it will also become a NOP (no operation instruction) if the script is not
run interactively.

**Parameters**
    - ``info`` *(Optional[str])* – The message to print before pausing. Defaults to "Press any key to proceed >> ..".


.. code:: python

    from quo import pause
    
    pause()



