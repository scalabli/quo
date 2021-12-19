#!/usr/bin/env python
"""
A simple example of a Notepad-like text editor.
"""
import datetime
import asyncio
import quo

from quo.suite.current import get_app
from quo.completion import PathCompleter
from quo.filters import Condition
from quo.layout.containers import (
    ConditionalContainer,
    Float
)
from quo.layout.controls import FormattedTextControl
from quo.layout.dimension import D
from quo.layout.menus import CompletionsMenu
from quo.lexers import DynamicLexer, PygmentsLexer
from quo.search import start_search
from quo.styles import Style
from quo.widgets import (
    Button,
    Dialog,
    Label,
    SearchToolbar,
    TextArea,
)


class ApplicationState:
    """
    Application state.

    For the simplicity, we store this as a global, but better would be to
    instantiate this as an object and pass at around.
    """

    show_status_bar = True
    current_path = None


def get_statusbar_text():
    return " Press Ctrl-C to open menu. "


def get_statusbar_right_text():
    return " {}:{}  ".format(
        text_field.document.cursor_position_row + 1,
        text_field.document.cursor_position_col + 1,
    )


search_toolbar = quo.widgets.SearchToolbar()
text_field = quo.widgets.TextArea(
    lexer=DynamicLexer(
        lambda: PygmentsLexer.from_filename(
            ApplicationState.current_path or ".txt", sync_from_start=False
        )
    ),
    scrollbar=True,
    line_numbers=True,
    search_field=search_toolbar,
)


class TextInputDialog:
    def __init__(self, title="", label_text="", completer=None):
        self.future = asyncio.Future()

        def accept_text(buf):
            get_app().layout.focus(ok_button)
            buf.complete_state = None
            return True

        def accept():
            self.future.set_result(self.text_area.text)

        def cancel():
            self.future.set_result(None)

        self.text_area = quo.widgets.TextArea(
            completer=completer,
            multiline=False,
            width=D(preferred=40),
            accept_handler=accept_text,
        )

        ok_button = quo.widgets.Button(text="OK", handler=accept)
        cancel_button = quo.widgets.Button(text="Cancel", handler=cancel)

        self.dialog = quo.layout.Dialog(
            title=title,
            body=quo.layout.HSplit([quo.widgets.Label(text=label_text), self.text_area]),
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            modal=True,
        )

    def __pt_container__(self):
        return self.dialog


class MessageDialog:
    def __init__(self, title, text):
        self.future = asyncio.Future()

        def set_done():
            self.future.set_result(None)

        ok_button = quo.widgets.Button(text="OK", handler=(lambda: set_done()))

        self.dialog = Dialog(
            title=title,
            body=quo.layout.HSplit([quo.widgets.Label(text=text)]),
            buttons=[ok_button],
            width=D(preferred=80),
            modal=True,
        )

    def __pt_container__(self):
        return self.dialog


body = quo.layout.HSplit(
    [
        text_field,
        search_toolbar,
        ConditionalContainer(
            content=quo.layout.VSplit(
                [
                    quo.layout.Window(
                        FormattedTextControl(get_statusbar_text), style="class:status"
                    ),
                    quo.layout.Window(
                        FormattedTextControl(get_statusbar_right_text),
                        style="class:status.right",
                        width=9,
                        align=quo.layout.WindowAlign.RIGHT,
                    ),
                ],
                height=1,
            ),
            filter=Condition(lambda: ApplicationState.show_status_bar),
        ),
    ]
)


# Global key bindings.
bindings = quo.keys.KeyBinder()


@bindings.add("ctrl-c")
def _(event):
    "Focus menu."
    event.app.layout.focus(root_container.window)


#
# Handlers for menu items.
#


def do_open_file():
    async def coroutine():
        open_dialog = TextInputDialog(
            title="Open file",
            label_text="Enter the path of a file:",
            completer=PathCompleter(),
        )

        path = await show_dialog_as_float(open_dialog)
        ApplicationState.current_path = path

        if path is not None:
            try:
                with open(path, "rb") as f:
                    text_field.text = f.read().decode("utf-8", errors="ignore")
            except IOError as e:
                show_message("Error", "{}".format(e))

    asyncio.ensure_future(coroutine())


def do_about():
    show_message("About", "Text editor demo.\nCreated by Gerrishon Sirere.")


def show_message(title, text):
    async def coroutine():
        dialog = MessageDialog(title, text)
        await show_dialog_as_float(dialog)

    asyncio.ensure_future(coroutine())


async def show_dialog_as_float(dialog):
    "Coroutine."
    float_ = Float(content=dialog)
    root_container.floats.insert(0, float_)

    app = get_app()

    focused_before = app.layout.current_window
    app.layout.focus(dialog)
    result = await dialog.future
    app.layout.focus(focused_before)

    if float_ in root_container.floats:
        root_container.floats.remove(float_)

    return result


def do_new_file():
    text_field.text = ""


def do_exit():
    get_app().exit()


def do_time_date():
    text = datetime.datetime.now().isoformat()
    text_field.buffer.insert_text(text)


def do_go_to():
    async def coroutine():
        dialog = TextInputDialog(title="Go to line", label_text="Line number:")

        line_number = await show_dialog_as_float(dialog)

        try:
            line_number = int(line_number)
        except ValueError:
            show_message("Invalid line number")
        else:
            text_field.buffer.cursor_position = (
                text_field.buffer.document.translate_row_col_to_index(
                    line_number - 1, 0
                )
            )

    asyncio.ensure_future(coroutine())


def do_undo():
    text_field.buffer.undo()


def do_cut():
    data = text_field.buffer.cut_selection()
    get_app().clipboard.set_data(data)


def do_copy():
    data = text_field.buffer.copy_selection()
    get_app().clipboard.set_data(data)


def do_delete():
    text_field.buffer.cut_selection()


def do_find():
    start_search(text_field.control)


def do_find_next():
    search_state = get_app().current_search_state

    cursor_position = text_field.buffer.get_search_position(
        search_state, include_current_position=False
    )
    text_field.buffer.cursor_position = cursor_position


def do_paste():
    text_field.buffer.paste_clipboard_data(get_app().clipboard.get_data())


def do_select_all():
    text_field.buffer.cursor_position = 0
    text_field.buffer.start_selection()
    text_field.buffer.cursor_position = len(text_field.buffer.text)


def do_status_bar():
    ApplicationState.show_status_bar = not ApplicationState.show_status_bar


#
# The menu container.
#


root_container = quo.widgets.MenuContainer(
    body=body,
    menu_items=[
        quo.widgets.MenuItem(
            "File",
            children=[
                quo.widgets.MenuItem("New...", handler=do_new_file),
                quo.widgets.MenuItem("Open...", handler=do_open_file),
                quo.widgets.MenuItem("Save"),
                quo.widgets.MenuItem("Save as..."),
                quo.widgets.MenuItem("-", disabled=True),
                quo.widgets.MenuItem("Exit", handler=do_exit),
            ],
        ),
        quo.widgets.MenuItem(
            "Edit",
            children=[
                quo.widgets.MenuItem("Undo", handler=do_undo),
                quo.widgets.MenuItem("Cut", handler=do_cut),
                quo.widgets.MenuItem("Copy", handler=do_copy),
                quo.widgets.MenuItem("Paste", handler=do_paste),
                quo.widgets.MenuItem("Delete", handler=do_delete),
                quo.widgets.MenuItem("-", disabled=True),
                quo.widgets.MenuItem("Find", handler=do_find),
                quo.widgets.MenuItem("Find next", handler=do_find_next),
                quo.widgets.MenuItem("Replace"),
                quo.widgets.MenuItem("Go To", handler=do_go_to),
                quo.widgets.MenuItem("Select All", handler=do_select_all),
                quo.widgets.MenuItem("Time/Date", handler=do_time_date),
            ],
        ),
        quo.widgets.MenuItem(
            "View",
            children=[quo.widgets.MenuItem("Status Bar", handler=do_status_bar)],
        ),
        quo.widgets.MenuItem(
            "Info",
            children=[quo.widgets.MenuItem("About", handler=do_about)],
        ),
    ],
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
        ),
    ],
    key_bindings=bindings,
)


style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#440044",
    }
)


layout = quo.layout.Layout(root_container, focused_element=text_field)


application = quo.Suite(
    layout=layout,
    enable_page_navigation_bindings=True,
    style=style,
    mouse_support=True,
    full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()
