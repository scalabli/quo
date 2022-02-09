.. _dialogs:

Dialogs
=======

quo ships with a high level API for displaying dialogs, similar to
the Whiptail program, but in pure Python.


``Message Box``
---------------

Use the :func:`~quo.MessageBox` function to display a
simple message box. For instance:

.. code:: python

    import quo

    quo.MessageBox(
        title='Example dialog window',
        text='Do you want to continue?\nPress ENTER to quit.').run()

.. image:: ./images/messagebox.png


``Prompt Box``
--------------

The :func:`~quo.PromptBox` function can display an
input box. It will return the user input as a string.

.. code:: python

    import quo

    quo.PromptBox(
        title='Input dialog example',
        text='Please type your name:').run()

.. image:: ./images/inputbox.png


The ``password=True`` option can be passed to the
:func:`~quo.PromptBox` function to turn this into a password input box.


``Confirmation Box``
--------------------

The :func:`~quo.ConfirmationBox` function displays a yes/no
confirmation dialog. It will return a boolean according to the selection.

.. code:: python

    import quo

    quo.ConfirmationBox(
        title='Yes/No dialog example',
        text='Do you want to confirm?').run()

.. image:: ./images/confirm.png


``Choice Box``
---------------

The :func:`~quo.ChoiceBox` function displays a dialog
with choices offered as buttons. Buttons are indicated as a list of tuples, each providing the label (first) and return value if clicked (second).

.. code:: python

    import quo

    quo.ChoiceBox(
        title='Button dialog example',
        text='Do you want to confirm?',
        buttons=[
            ('Yes', True),
            ('No', False),
            ('Maybe...', None)
        ],).run()

.. image:: ./images/button.png


``Radiolist Box``
-----------------

The :func:`~quo.RadiolistBox` function displays a dialog
with choices offered as a radio list. The values are provided as a list of tuples,
each providing the return value (first element) and the displayed value (second element).

.. code:: python

    import quo

    quo.RadiolistBox( 
        title="RadioList dialog", 
        text="Which breakfast would you like ?", 
        values=[ 
            ("breakfast1", "Eggs and beacon"), 
            ("breakfast2", "French breakfast"), 
            ("breakfast3", "Equestrian breakfast") 
        ]).run()


``Check Box``
-------------

The :func:`~quo.CheckBox` has the same usage and purpose than the Radiolist dialog, but allows several values to be selected and therefore returned.

.. code:: python

    import quo

    results_array = quo.CheckBox( 
        title="CheckboxList dialog", 
        text="What would you like in your breakfast ?",
        values=[ 
            ("eggs", "Eggs"),
            ("bacon", "Bacon"),
            ("croissants", "20 Croissants"),
            ("daily", "The breakfast of the day")
        ] 
    ).run()


Styling of dialogs
------------------

A custom :class:`~quo.styles.Style` instance can be passed to all
dialogs to override the default style. Also, text can be styled by passing an
:class:`~quo.text.HTML` object.


.. code:: python

    import quo

    style = quo.styles.Style

    example_style = style.add({
        'dialog':             'bg:#88ff88',
        'dialog frame.label': 'bg:#ffffff #000000',
        'dialog.body':        'bg:#000000 #00ff00',
        'dialog shadow':      'bg:#00aa00',
    })

    quo.MessageBox(
        title=quo.text.HTML('<style bg="blue" fg="white">Styled</style> '
                   '<style fg="ansired">dialog</style> window'),
        text='Do you want to continue?\nPress ENTER to quit.',
        style=example_style).run()

.. image:: ./images/styled.png

Styling reference sheet
-----------------------

In reality, the shortcut commands presented above build a full-screen frame by using a list of components. The two tables below allow you to get the classnames available for each shortcut, therefore you will be able to provide a custom style for every element that is displayed, using the method provided above.

.. note:: All the shortcuts use the ``Dialog`` component, therefore it isn't specified explicitly below.

+-------------------------+-------------------------+
| Shortcut                | Components used         |
+=========================+=========================+
| ``quo.ConfirmationBox`` | - ``Label``             |
|                         | - ``Button`` (x2)       |
+-------------------------+-------------------------+
| ``quo.ChoiceBox``       | - ``Label``             |
|                         | - ``Button``            |
+-------------------------+-------------------------+
| ``quo.PromptBox``       | - ``TextArea``          |
|                         | - ``Button`` (x2)       |
+-------------------------+-------------------------+
| ``quo.MessageBox``      | - ``Label``             |
|                         | - ``Button``            |
+-------------------------+-------------------------+
| ``quo.RadiolistBox``    | - ``Label``             |
|                         | - ``RadioList``         |
|                         | - ``Button`` (x2)       |
+-------------------------+-------------------------+
| ``quo.CheckBox``        | - ``Label``             |
|                         | - ``CheckboxList``      |
|                         | - ``Button`` (x2)       |
+-------------------------+-------------------------+
| ``quo.ProgressBox``     | - ``Label``             |
|                         | - ``TextArea`` (locked) |
|                         | - ``ProgressBar``       |
+-------------------------+-------------------------+

+----------------+------------------------+
| Components     | Available classnames   |
+================+========================+
| Dialog         | - ``dialog``           |
|                | - ``dialog.body``      |
+----------------+------------------------+
| TextArea       | - ``text-area``        |
|                | - ``text-area.prompt`` |
+----------------+------------------------+
| Label          | - ``label``            |
+----------------+------------------------+
| Button         | - ``button``           |
|                | - ``button.focused``   |
|                | - ``button.arrow``     |
|                | - ``button.text``      |
+----------------+------------------------+
| Frame          | - ``frame``            |
|                | - ``frame.border``     |
|                | - ``frame.label``      |
+----------------+------------------------+
| Shadow         | - ``shadow``           |
+----------------+------------------------+
| RadioList      | - ``radio-list``       |
|                | - ``radio``            |
|                | - ``radio-checked``    |
|                | - ``radio-selected``   |
+----------------+------------------------+
| CheckboxList   | - ``checkbox-list``    |
|                | - ``checkbox``         |
|                | - ``checkbox-checked`` |
|                | - ``checkbox-selected``|
+----------------+------------------------+
| VerticalLine   | - ``line``             |
|                | - ``vertical-line``    |
+----------------+------------------------+
| HorizontalLine | - ``line``             |
|                | - ``horizontal-line``  |
+----------------+------------------------+
| ProgressBar    | - ``progress-bar``     |
|                | - ``progress-bar.used``|
+----------------+------------------------+

Example
_______

Let's customize the example of the ``checkbox``.

It uses 2 ``Button``, a ``CheckboxList`` and a ``Label``, packed inside a ``Dialog``.
Therefore we can customize each of these elements separately, using for instance:

.. code:: python

    import quo

    styles = quo.styles.Style

    quo.CheckBox(
        title="CheckboxList dialog",
        text="What would you like in your breakfast ?",
        values=[
            ("eggs", "Eggs"),
            ("bacon", "Bacon"),
            ("croissants", "20 Croissants"),
            ("daily", "The breakfast of the day")
        ],
        style = styles.add({
            'dialog': 'bg:#cdbbb3',
            'button': 'bg:#bf99a4',
            'checkbox': '#e8612c',
            'dialog.body': 'bg:#a9cfd0',
            'dialog shadow': 'bg:#c98982',
            'frame.label': '#fcaca3',
            'dialog.body label': '#fd8bb6',
        })).run()
