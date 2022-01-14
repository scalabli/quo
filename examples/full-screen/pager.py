#!/usr/bin/env python
"""
A simple application that shows a Pager application.
"""

import quo
from pygments.lexers.python import PythonLexer

from quo.layout.containers import HSplit, Window
from quo.layout.controls import FormattedTextControl
from quo.layout.dimension import LayoutDimension as D
from quo.lexers import PygmentsLexer
# Create one text buffer for the main content.

_pager_py_path = __file__


with open(_pager_py_path, "rb") as f:
    text = f.read().decode("utf-8")


def get_statusbar_text():
    return [
        ("class:status", _pager_py_path + " - "),
        (
            "class:status.position",
            "{}:{}".format(
                text_area.document.cursor_position_row + 1,
                text_area.document.cursor_position_col + 1,
            ),
        ),
        ("class:status", " - Press "),
        ("class:status.key", "Ctrl-C"),
        ("class:status", " to exit, "),
        ("class:status.key", "/"),
        ("class:status", " for searching."),
    ]


search_field = quo.widgets.SearchToolbar(
    text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")]
)


text_area = quo.widgets.TextArea(
    text=text,
    read_only=True,
    scrollbar=True,
    line_numbers=True,
    search_field=search_field,
    lexer=PygmentsLexer(PythonLexer),
)


root_container = HSplit(
    [
        # The top toolbar.
        Window(
            content=FormattedTextControl(get_statusbar_text),
            height=D.exact(1),
            style="class:status",
        ),
        # The main content.
        text_area,
        search_field,
    ]
)


# Key bindings.
bindings = quo.keys.KeyBinder()


@bindings.add("ctrl-c")
@bindings.add("q")
def _(event):
    "Quit."
    event.app.exit()


style = quo.styles.Style.from_dict(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)

layout = quo.layout.Layout(root_container, focused_element=text_area)

# create application.

application = quo.Suite(
    layout=layout,
    bind=bindings,
    enable_page_navigation_bindings=True,
    mouse_support=True,
    style=style,
    full_screen=True,
    )


def run():
    application.run()


if __name__ == "__main__":
    run()
