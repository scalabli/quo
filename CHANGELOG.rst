.. currentmodule:: quo

Version 2021.4
-------------

Unreleased


Version 2021.3
-------------

Unreleased

-   ``foreground`` and ``background`` changed to ``fg`` and ``bg`` 

-   Added support for lively ``ProgressBars``

-   Minimal implementation of ``HTML`` module to easy formating

-   Fixed changelong link on PyPI



Version 2021.2
-------------

Released 2021-06-28

-   Mark top-level names as exported so type checking understand imports
    in user projects. :issue:`1879`
-   Annotate ``Context.obj`` as ``Any`` so type checking allows all
    operations on the arbitrary object. :issue:`1885`
-   Fix some types that weren't available in Python 3.6.0. :issue:`1882`
-   Fix type checking for iterating over ``ProgressBar`` object.
    :issue:`1892`
-   ``importlib_metadata`` backport package is installed on Python <
    3.8 therefore will be be delisted as part of Quo's external dependency in later versions of Quo
-   Arguments with ``nargs=-1`` only use env var value if no command
    line values are given. :issue:`1903`
-   Flag options guess their type from ``flag_value`` if given, like
    regular options do from ``default``. :issue:`1886`
-   Added documentation that custom parameter types may be passed
    already valid values in addition to strings. :issue:`1898`
-   Resolving commands returns the name that was given, not
    ``command.name``, fixing an unintended change to help text and
    ``default_map`` lookups. When using patterns like ``AliasedGroup``,
    override ``resolve_command`` to change the name that is returned if
    needed. :issue:`1895`
-   If a default value is invalid, it does not prevent showing help
    text. :issue:`1889`
-   Pass ``windows_expand_args=False`` when calling the main command to
    disable pattern expansion on Windows. There is no way to escape
    patterns in CMD, so if the program needs to pass them on as-is then
    expansion must be disabled. :issue:`1901`


Version 2021.1
---------------
Released 2021-06-18

+  ``command``
-  ``app``
-  ``confirm``
-  ``prompt``
-  ``flair``
-   Added support for ``ANSI colors`` for better coloring of the terminal

