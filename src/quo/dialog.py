import functools
from asyncio import get_event_loop
from typing import Any, Callable, List, Optional, Tuple, TypeVar

from quo.console.console import Console
from quo.console.current import get_app
from quo.completion.core import Completer
from quo.eventloop import run_in_executor_with_context
from quo.filters.core import FilterOrBool
from quo.text.core import AnyFormattedText
from quo.layout.layout import Layout
from quo.layout.containers import AnyContainer, HSplit
from quo.layout.dimension import Dimension as D
from quo.style.core import BaseStyle
from quo.types import Validator
from quo.widget import (
    Box,
    Button,
    #  CheckboxList,
    Dialog,
    Label,
    #    ProgressBar,
    #   RadioList
)

__all__ = [
    "ConfirmBox",
    "ChoiceBox",
    "InputBox",
    "MessageBox",
    "RadiolistBox",
    "CheckBox",
    "ProgressBox",
]


def _ConfirmationBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    yes_text: str = "Yes",
    no_text: str = "No",
    bg: bool = True,
    style: Optional[BaseStyle] = None,
) -> Console[bool]:
    """
    Display a Yes/No dialog.
    Return a boolean.
    """

    def yes_handler() -> None:
        get_app().exit(result=True)

    def no_handler() -> None:
        get_app().exit(result=False)

    if bg is False:
        dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[
                Button(text=yes_text, handler=yes_handler),
                Button(text=no_text, handler=no_handler),
            ],
            with_background=False,
        )
    else:
        dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[
                Button(text=yes_text, handler=yes_handler),
                Button(text=no_text, handler=no_handler),
            ],
            with_background=True,
        )  

    return _create_app(dialog, style)


_T = TypeVar("_T")


def _ChoiceBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    buttons: List[Tuple[str, _T]] = [],
    style: Optional[BaseStyle] = None,
    bg: bool = True,
) -> Console[_T]:
    """
    Display a dialog with button choices (given as a list of tuples).
    Return the value associated with button.
    """

    def button_handler(v: _T) -> None:
        get_app().exit(result=v)

    if bg is False:
        dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[
                Button(text=t, handler=functools.partial(button_handler, v))
                for t, v in buttons
            ],
            with_background=False,
        )
    else:
        dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[
                Button(text=t, handler=functools.partial(button_handler, v))
                for t, v in buttons
            ],
            with_background=True,
        )

    return _create_app(dialog, style)


def _PromptBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    completer: Optional[Completer] = None,
    type: Optional[Validator] = None,
    hide: FilterOrBool = False,
    multiline: bool = False,
    bg=True,
    style: Optional[BaseStyle] = None,
) -> Console[str]:
    """
    Display a text input box.
    Return the given text, or None when cancelled.
    """
    from .buffer import Buffer
    from .widget.core import TextArea
    from .widget.toolbars import ValidationToolbar

    def accept(buf: Buffer) -> bool:
        get_app().layout.focus(ok_button)
        return True  # Keep text.

    def ok_handler() -> None:
        get_app().exit(result=textfield.text)

    ok_button = Button(text=ok_text, handler=ok_handler)
    cancel_button = Button(text=cancel_text, handler=_return_none)

    textfield = TextArea(
        multiline=multiline,
        hide=hide,
        completer=completer,
        type=type,
        accept_handler=accept,
    )

    dialog = Dialog(
        title=title,
        body=HSplit(
            [
                Label(text=text, dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        ),
        buttons=[ok_button, cancel_button],
        with_background=True,
    )
    if bg is False:
        dialog = Dialog(
            title=title,
            body=HSplit(
                [
                    Label(text=text, dont_extend_height=True),
                    textfield,
                    ValidationToolbar(),
                ],
                padding=D(preferred=1, max=1),
            ),
            buttons=[ok_button, cancel_button],
            with_background=False,
        )

    return _create_app(dialog, style)


def _MessageBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    style: Optional[BaseStyle] = None,
    bg: bool = True,
) -> Console[None]:
    """
    Display a simple message box and wait until the user presses enter.
    """
    dialog = Dialog(
        title=title,
        body=Label(text=text, dont_extend_height=True),
        buttons=[Button(text=ok_text, handler=_return_none)],
        with_background=True,
    )
    if bg is False:
        dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[Button(text=ok_text, handler=_return_none)],
            with_background=False,
        )

    return _create_app(dialog, style)


def _RadiolistBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, AnyFormattedText]]] = None,
    bg: bool = True,
    style: Optional[BaseStyle] = None,
) -> Console[_T]:
    """
    Display a simple list of element the user can choose amongst.

    Only one element can be selected at a time using Arrow keys and Enter.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    from .widget.core import RadioList

    if values is None:
        values = []

    def ok_handler() -> None:
        get_app().exit(result=radio_list.current_value)

    radio_list = RadioList(values)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=text, dont_extend_height=True), radio_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        with_background=True,
    )

    return _create_app(dialog, style)


def _CheckBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, AnyFormattedText]]] = None,
    bg: bool = True,
    style: Optional[BaseStyle] = None,
) -> Console[List[_T]]:
    """
    Display a simple list of element the user can choose multiple values amongst.

    Several elements can be selected at a time using Arrow keys and Enter.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    from .widget.core import CheckboxList

    if values is None:
        values = []

    def ok_handler() -> None:
        get_app().exit(result=cb_list.current_values)

    cb_list = CheckboxList(values)

    if bg is False:
        dialog = Dialog(
            title=title,
            body=HSplit(
                [Label(text=text, dont_extend_height=True), cb_list], padding=1
            ),
            buttons=[
                Button(text=ok_text, handler=ok_handler),
                Button(text=cancel_text, handler=_return_none),
            ],
            with_background=False,
        )

    else:
        dialog = Dialog(
            title=title,
            body=HSplit(
                [Label(text=text, dont_extend_height=True), cb_list], padding=1
            ),
            buttons=[
                Button(text=ok_text, handler=ok_handler),
                Button(text=cancel_text, handler=_return_none),
            ],
            with_background=True,
        )

    return _create_app(dialog, style)


def _ProgressBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    bg: bool = True,
    run_callback: Callable[[Callable[[int], None], Callable[[str], None]], None] = (
        lambda *a: None
    ),
    style: Optional[BaseStyle] = None,
) -> Console[None]:
    """
    :param run_callback: A function that receives as input a `set_percentage` function and it does the work.
    """
    from .widget.core import ProgressBar, TextArea

    loop = get_event_loop()
    progressbar = ProgressBar()
    text_area = TextArea(
        focusable=False,
        # Prefer this text area as big as possible, to avoid having a window
        # that keeps resizing when we add text to it.
        height=D(preferred=10**10),
    )

    if bg is False:
        dialog = Dialog(
            body=HSplit(
                [Box(Label(text=text)), Box(text_area, padding=D.exact(1)), progressbar]
            ),
            title=title,
            with_background=False,
        )

    else:
        dialog = Dialog(
            body=HSplit(
                [Box(Label(text=text)), Box(text_area, padding=D.exact(1)), progressbar]
            ),
            title=title,
            with_background=True,
        )

    app = _create_app(dialog, style)

    def set_percentage(value: int) -> None:
        progressbar.percentage = int(value)
        app.invalidate()

    def log_text(text: str) -> None:
        loop.call_soon_threadsafe(text_area.buffer.insert_text, text)
        app.invalidate()

    # Run the callback in the executor. When done, set a return value for the
    # UI, so that it quits.
    def start() -> None:
        try:
            run_callback(set_percentage, log_text)
        finally:
            app.exit()

    def pre_run() -> None:
        run_in_executor_with_context(start)

    app.pre_run_callables.append(pre_run)

    return app


def _create_app(dialog: AnyContainer, style: Optional[BaseStyle]) -> Console[Any]:
    # Key bindings.
    from .keys.key_binding.key_bindings import Bind
    from quo.keys.key_binding.bindings.focus import next, previous
    from quo.keys.key_binding.defaults import load_key_bindings
    from quo.keys.key_binding.key_bindings import merge_key_bindings

    bindings = Bind()
    bindings.add("tab")(next)
    bindings.add("s-tab")(previous)

    return Console(
        layout=Layout(dialog),
        bind=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )


def _return_none() -> None:
    "Button handler that returns None."
    get_app().exit()


# High level dialog API


def CheckBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, AnyFormattedText]]] = None,
    bg: bool = True,
    style: Optional[BaseStyle] = None,
):
    _CheckBox(
        title=title,
        text=text,
        ok_text=ok_text,
        cancel_text=cancel_text,
        values=values,
        style=style,
    ).run()


def ChoiceBox(
    title: str = "", text: str = "", buttons=[], bg: bool = True, style: Optional = None
):
    _ChoiceBox(title=title, text=text, buttons=buttons, bg=bg, style=style).run()


def ConfirmBox(
    title="",
    text="",
    yes_text: str = "Yes",
    no_text: str = "No",
    bg: bool = True,
    style: Optional = None,
):
    return _ConfirmationBox(
        title=title, text=text, yes_text=yes_text, no_text=no_text, bg=bg, style=style
    ).run()


def InputBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    completer: Optional[Completer] = None,
    type: Optional[Validator] = None,
    hide: FilterOrBool = False,
    multiline: bool = False,
    bg=True,
    style: Optional[BaseStyle] = None,
):

    return _PromptBox(
        title=title,
        text=text,
        ok_text=ok_text,
        cancel_text=cancel_text,
        completer=completer,
        type=type,
        hide=hide,
        multiline=multiline,
        bg=bg,
        style=style,
    ).run()


def MessageBox(title="", text="", ok_text: str = "Ok", style=None, bg: bool = True):

    return _MessageBox(
        title=title, text=text, ok_text=ok_text, bg=bg, style=style
    ).run()


def ProgressBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    bg: bool = True,
    run_callback: Callable[[Callable[[int], None], Callable[[str], None]], None] = (
        lambda *a: None
    ),
    style: Optional[BaseStyle] = None,
):

    return _ProgressBox(
        title=title, text=text, bg=bg, run_callback=run_callback, style=style
    ).run()


def RadiolistBox(
    title: AnyFormattedText = "",
    text: AnyFormattedText = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, AnyFormattedText]]] = None,
    style: Optional[BaseStyle] = None,
):
    _RadiolistBox(
        title=title,
        text=text,
        ok_text=ok_text,
        cancel_text=cancel_text,
        values=values,
        style=style,
    ).run()


# For backward compatibility
PromptBox = InputBox
ConfirmationBox = ConfirmBox
