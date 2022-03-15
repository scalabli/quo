Exception(Error) Handling
==========================

.. currentmodule:: quo

Quo internally uses exceptions to signal various error conditions that
the user of the application might have caused.  Primarily this is things
like incorrect usage.

``Where are Errors Handled?``
----------------------------

Quo's main error handling is happening in :meth:`BaseCommand.main`.  In
there it handles all subclasses of :exc:`Outlier` as well as the standard :exc:`EOFError` and :exc:`KeyboardInterrupt` exceptions.  The
latter are internally translated into a :exc:`Abort`.

The logic applied is the following:

1.  If an :exc:`EOFError` or :exc:`KeyboardInterrupt` happens, reraise it
    as :exc:`Abort`.
2.  If an :exc:`Outlier` is raised, invoke the
    :meth:`Outlier.show` method on it to display it and then exit
    the program with :attr:`Outlier.exit_code`.
3.  If an :exc:`Abort` exception is raised print the string ``Aborted!``
    to standard error and exit the program with exit code ``1``.
4.  if it goes through well, exit the program with exit code ``0``.


``Which Exceptions Exist?``
---------------------------

Quo has two exception bases: :exc:`Outlier` which is raised for
all exceptions that quo wants to signal to the user and :exc:`Abort`
which is used to instruct quo to abort the execution.

A :exc:`Outlier` has a :meth:`~Outlier.show` method which
can render an error message to stderr or the given file object.  If you
want to use the exception yourself for doing something check the API docs
about what else they provide.

The following common subclasses exist:

*   :exc:`UsageError` to inform the user that something went wrong.
*   :exc:`BadParameter` to inform the user that something went wrong with
    a specific parameter.  These are often handled internally in quo and
    augmented with extra information if possible.  For instance if those
    are raised from a callback quo will automatically augment it with
    the parameter name if possible.
*   :exc:`FileError` this is an error that is raised by the :exc:`FileType` if quo encounters issues opening the file.
*   :exc:`ValidationError` if quo encounters issues validating an input.
