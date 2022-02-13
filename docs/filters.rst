.. _filters:

Filters
=========

Many places in `quo` require a boolean value that can change over
time. For instance:

- to specify whether a formatred text needs to be bold or in italic.
- to specify whether a part of the layout needs to be visible or not;
- or to decide whether a certain key binding needs to be active or not.

These booleans are often dynamic and can change at runtime. For instance, the
search toolbar should only be visible when the user is actually searching (when
the search buffer has the focus). The ``wrap_lines`` option could be changed
with a certain key binding. And that key binding could only work when the
default buffer got the focus.

In `quo`, we decided to reduce the amount of state in the whole
framework, and apply a simple kind of reactive programming to describe the flow
of these booleans as expressions. (It's one-way only: if a key binding needs to
know whether it's active or not, it can follow this flow by evaluating an
expression.)

The (abstract) base class is :class:`~quo.filters.Filter`, which
wraps an expression that takes no input and evaluates to a boolean. Getting the
state of a filter is done by simply calling it.


An example
----------

The most obvious way to create such a :class:`~quo.filters.Filter`
instance is by creating a :class:`~quo.filters.Condition` instance
from a function. For instance, the following condition will evaluate to ``True`` when the user is searching:

.. code:: python

    from quo import Condition
    from quo.console import get_app

    @Condition
    def is_searching():
        return get_app().is_searching

This filter can then be used in a key binding, like in the following snippet:

.. code:: python

    from quo.keys import KeyBinder

    kb = KeyBinder()

    @kb.add('ctrl-t', filter=is_searching)
    def _(event):
        # Do, something, but only when searching.
        pass

If we want to know the boolean value of this filter, we have to call it like a
function:

.. code:: python

    print(is_searching())


Built-in filters
----------------

There are many built-in filters, ready to use. All of them have a lowercase
name, because they represent the wrapped function underneath, and can be called
as a function.

- :class:`~quo.filters.app.has_arg`
- :class:`~quo.filters.app.has_completions`
- :class:`~quo.filters.app.has_focus`
- :class:`~quo.filters.app.buffer_has_focus`
- :class:`~quo.filters.app.has_selection`
- :class:`~quo.filters.app.has_validation_error`
- :class:`~quo.filters.app.is_aborting`
- :class:`~quo.filters.app.is_done`
- :class:`~quo.filters.app.is_read_only`
- :class:`~quo.filters.app.is_multiline`
- :class:`~quo.filters.app.renderer_height_is_known`
- :class:`~quo.filters.app.in_editing_mode`
- :class:`~quo.filters.app.in_paste_mode`

- :class:`~quo.filters.app.vi_mode`
- :class:`~quo.filters.app.vi_navigation_mode`
- :class:`~quo.filters.app.vi_insert_mode`
- :class:`~quo.filters.app.vi_insert_multiple_mode`
- :class:`~quo.filters.app.vi_replace_mode`
- :class:`~quo.filters.app.vi_selection_mode`
- :class:`~quo.filters.app.vi_waiting_for_text_object_mode`
- :class:`~quo.filters.app.vi_digraph_mode`

- :class:`~quo.filters.app.emacs_mode`
- :class:`~quo.filters.app.emacs_insert_mode`
- :class:`~quo.filters.app.emacs_selection_mode`

- :class:`~quo.filters.app.is_searching`
- :class:`~quo.filters.app.control_is_searchable`
- :class:`~quo.filters.app.vi_search_direction_reversed`


Combining filters
-----------------

Filters can be chained with the ``&`` (AND) and ``|`` (OR) operators and
negated with the ``~`` (negation) operator.

Some examples:

.. code:: python

    from quo.keys import KeyBinder

    kb = KeyBinder()

    @kb.add('ctrl-t', filter=~is_searching)
    def _(event):
        " Do something, but not while searching. "
        pass

    @kb.add('ctrl-t', filter=has_search | has_selection)
    def _(event):
        " Do something, but only when searching or when there is a selection. "
        pass


to_filter
---------

Finally, in many situations you want your code to expose an API that is able to
deal with both booleans as well as filters. For instance, when for most users a
boolean works fine because they don't need to change the value over time, while
some advanced users want to be able this value to a certain setting or event
that does changes over time.

In order to handle both use cases, there is a utility called
:func:`~quo.filters.to_filter`.

This is a function that takes
either a boolean or an actual :class:`~quo.filters.Filter`
instance, and always returns a :class:`~quo.filters.Filter`.

.. code:: python

    import quo

    # In each of the following three examples, 'f' will be a `Filter`
    # instance.
    f = quo.filters.to_filter(True)
    f = quo.filters.to_filter(False)
    f = quo.filters.to_filter(quo.filters.Condition(lambda: True))
    f = quo.filters.to_filter(quo.filters.has_search | quo.filters.has_selection)
