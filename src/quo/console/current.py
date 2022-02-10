import sys
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Generator, Optional

try:
    from contextvars import ContextVar
except ImportError:
    from quo.eventloop.dummy_contextvars import ContextVar  # type: ignore

if TYPE_CHECKING:
    from quo.input.core import Input
    from quo.output.core import Output

    from .console import Console

__all__ = [
        "AppSession",
        "get_app_session",
        "get_app",
        "get_app_or_none",
        "set_app",
        "create_app_session",
        ]


class AppSession:
    """
    An AppSession is an interactive session, usually connected to one terminal.
    Within one such session, interaction with many applications can happen, one
    after the other.

    The input/output device is not supposed to change during one session.

    Warning: Always use the `create_app_session` function to create an
    instance, so that it gets activated correctly.

    :param input: Use this as a default input for all applications
        running in this session, unless an input is passed to the `Application`
        explicitely.
    :param output: Use this as a default output.
    """

    def __init__(
        self, input: Optional["Input"] = None, output: Optional["Output"] = None
    ) -> None:

        self._input = input
        self._output = output

        # The application will be set dynamically by the `set_app` context
        # manager. This is called in the application itself.
        self.app: Optional["Console[Any]"] = None

    def __repr__(self) -> str:
        return "AppSession(app=%r)" % (self.app,)

    @property
    def input(self) -> "Input":
        if self._input is None:
            from quo.input.defaults import create_input

            self._input = create_input()
        return self._input

    @property
    def output(self) -> "Output":
        if self._output is None:
            from quo.output.defaults import create_output

            self._output = create_output()
        return self._output


_current_app_session: ContextVar["AppSession"] = ContextVar(
    "_current_app_session", default=AppSession()
)


def get_app_session() -> AppSession:
    return _current_app_session.get()


def get_app() -> "Console[Any]":
    """
    Get the current active (running) Application.
    An :class:`.Console` is active during the
    :meth:`.Console.run_async` call.

    We assume that there can only be one :class:`.Application` active at the
    same time. There is only one terminal window, with only one stdin and
    stdout. This makes the code significantly easier than passing around the
    :class:`.Console` everywhere.

    If no :class:`.Console` is running, then return by default a
    :class:`.DummyApplication`. For practical reasons, we prefer to not raise
    an exception. This way, we don't have to check all over the place whether
    an actual `Console` was returned.
    """
    session = _current_app_session.get()
    if session.app is not None:
        return session.app

    from .dummy import DummyApplication

    return DummyApplication()


def get_app_or_none() -> Optional["Console[Any]"]:
    """
    Get the current active (running) Application, or return `None` if no
    application is running.
    """
    session = _current_app_session.get()
    return session.app


@contextmanager
def set_app(app: "Console[Any]") -> Generator[None, None, None]:
    """
    Context manager that sets the given :class:`.Console` active in an
    `AppSession`.

    This should only be called by the `Console` itself.
    The application will automatically be active while its running. If you want
    the application to be active in other threads/coroutines, where that's not
    the case, use `contextvars.copy_context()`, or use `Suite.context` to
    run it in the appropriate context.
    """
    session = _current_app_session.get()

    previous_app = session.app
    session.app = app
    try:
        yield
    finally:
        session.app = previous_app


@contextmanager
def create_app_session(
    input: Optional["Input"] = None, output: Optional["Output"] = None
) -> Generator[AppSession, None, None]:
    """
    Create a separate AppSession.

    This is useful if there can be multiple individual `AppSession`s going on.
    Like in the case of an Telnet/SSH server. This functionality uses
    contextvars and requires at least Python 3.7.
    """
    if sys.version_info <= (3, 6):
        raise RuntimeError("This session requires Python 3.7 or later.")

    # If no input/output is specified, fall back to the current input/output,
    # whatever that is.
    if input is None:
        input = get_app_session().input
    if output is None:
        output = get_app_session().output

    # Create new `AppSession` and activate.
    session = AppSession(input=input, output=output)

    token = _current_app_session.set(session)
    try:
        yield session
    finally:
        _current_app_session.reset(token)
