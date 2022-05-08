#!/usr/bin/env python
"""
A simple application that shows a Pager application.
"""

from quo import container
from pygments.lexers.python import PythonLexer

#from prompt_toolkit.application import Application
from quo.layout.containers import HSplit, Window
from quo.layout.controls import FormattedTextControl
from quo.layout.dimension import LayoutDimension as D
from quo.layout.layout import Layout
from quo.highlight import PygmentsLexer
from quo.style import Style
from quo.widget import Label, SearchToolbar, TextArea

# Create one text buffer for the main content.

_pager_py_path = __file__

_file = "/root/git/quo/setup.py"
with open(_file, "rb") as f:
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


search_field = SearchToolbar(
    text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")]
)

text_ = Window(FormattedTextControl(f"{text}"))
text_area = TextArea(
    text,
    read_only=True,
    scrollbar=False,
    line_numbers=True,
    multiline=True,
    search_field=search_field,
    highlighter=PygmentsLexer(PythonLexer),
)

content = HSplit(
    [
        # The top toolbar.
        Window(
            content=FormattedTextControl(get_statusbar_text),
            height=D.exact(1),
            style="class:status",
        ),
        # The main content.
        text_area,
       # text_,
        search_field,
    ]
)


style = Style.add(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)


# create application.
#application = Application(
#    layout=Layout(root_container, focused_element=text_area),
#    key_bindings=bindings,
#    enable_page_navigation_bindings=True,
#    mouse_support=True,
 #   style=style,
#    full_screen=True,


def run():
    container(
            content,
            bind=True,
            focused_element=text_area,
            full_screen=True,
            style=style
            )


if __name__ == "__main__":
    run()
