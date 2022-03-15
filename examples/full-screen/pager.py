#!/usr/bin/env python
"""
A simple application that shows a Pager application.
"""


from quo.console import Console
from quo.keys import Bind
from quo.layout import HSplit, Window, Layout
from quo.layout.controls import FormattedTextControl
from quo.layout.dimension import LayoutDimension as D
from quo.widget import TextArea, SearchToolbar
from quo.highlight import Python
from quo.style import Style
# Create one text buffer for the main content.

with open(__file__, "rb") as f:
    text = f.read().decode("utf-8")


def get_statusbar_text():
    return [
        ("reverse", __file__ + " - "),
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


search_field =  SearchToolbar(
    text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")]
)


text_area = TextArea(
    text=text,
    read_only=True,
    scrollbar=True,
    line_numbers=True,
    search_field=search_field,
    highlighter=Python,
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
bindings = Bind()


@bindings.add("ctrl-c")
@bindings.add("q")
def _(event):
    "Quit."
    event.app.exit()


style = Style.add(
    {
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)

layout = Layout(root_container, focused_element=text_area)

# create application.

Console(
    layout=layout,
    bind=bindings,
    enable_page_navigation_bindings=True,
    mouse_support=True,
    style=style,
   # full_screen=True,
    ).run()
