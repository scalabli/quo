#!/usr/bin/env python
"""
"""

from quo import container
from quo.console import get_app
from quo.completion import WordCompleter
from quo.keys import bind, focus
from quo.layout.containers import Float, HSplit, VSplit
from quo.layout.dimension import D
from quo.layout.menus import CompletionsMenu
from quo.highlight import HTML as Html
from quo.style import Style
from quo.widget import (
    Box,
    Button,
    Checkbox,
    Dialog,
    Frame,
    Label,
    MenuContainer,
    MenuItem,
    ProgressBar,
    RadioList,
    TextArea,
)


def accept_yes():
    get_app().exit(result=True)


def accept_no():
    get_app().exit(result=False)


def do_exit():
    get_app().exit(result=False)


yes_button = Button(text="Yes", handler=accept_yes)
no_button = Button(text="No", handler=accept_no)
textfield = TextArea(highlighter=Html)
checkbox1 = Checkbox(text="Checkbox")
checkbox2 = Checkbox(text="Checkbox")

radios = RadioList(
    values=[
        ("Red", "red"),
        ("Green", "green"),
        ("Blue", "blue"),
        ("Orange", "orange"),
        ("Yellow", "yellow"),
        ("Purple", "Purple"),
        ("Brown", "Brown"),
    ]
)

animal_completer = WordCompleter(
    [
        "alligator",
        "ant",
        "ape",
        "bat",
        "bear",
        "beaver",
        "bee",
        "bison",
        "butterfly",
        "cat",
        "chicken",
        "crocodile",
        "dinosaur",
        "dog",
        "dolphin",
        "dove",
        "duck",
        "eagle",
        "elephant",
        "fish",
        "goat",
        "gorilla",
        "kangaroo",
        "leopard",
        "lion",
        "mouse",
        "rabbit",
        "rat",
        "snake",
        "spider",
        "turkey",
        "turtle",
    ],
    ignore_case=True,
)

root = HSplit(
    [
        VSplit(
            [
                Frame(body=Label(text="Left frame\ncontent")),
                Dialog(title="The custom window", body=Label("hello\ntest")),
                textfield,
            ],
            height=D(),
        ),
        VSplit(
            [
                Frame(body=ProgressBar(), title="Progress bar"),
                Frame(
                    title="Checkbox list",
                    body=HSplit([checkbox1, checkbox2]),
                ),
                Frame(title="Radio list", body=radios),
            ],
            padding=1,
        ),
        Box(
            body=VSplit([yes_button, no_button], align="CENTER", padding=3),
            style="class:button-bar",
            height=3,
        ),
    ]
)

content = MenuContainer(
    body=root,
    menu_items=[
        MenuItem(
            "File",
            subset=[
                MenuItem("New"),
                MenuItem(
                    "Open",
                    subset=[
                        MenuItem("From file..."),
                        MenuItem("From URL..."),
                        MenuItem(
                            "Something else..",
                            subset=[
                                MenuItem("A"),
                                MenuItem("B"),
                                MenuItem("C"),
                                MenuItem("D"),
                                MenuItem("E"),
                            ],
                        ),
                    ],
                ),
                MenuItem("Save"),
                MenuItem("Save as..."),
                MenuItem("-", disabled=True),
                MenuItem("Exit", handler=do_exit),
            ],
        ),
        MenuItem(
            "Edit",
            subset=[
                MenuItem("Undo"),
                MenuItem("Cut"),
                MenuItem("Copy"),
                MenuItem("Paste"),
                MenuItem("Delete"),
                MenuItem("-", disabled=True),
                MenuItem("Find"),
                MenuItem("Find next"),
                MenuItem("Replace"),
                MenuItem("Go To"),
                MenuItem("Select All"),
                MenuItem("Time/Date"),
            ],
        ),
        MenuItem("View", subset=[MenuItem("Status Bar")]),
        MenuItem("Info", subset=[MenuItem("About")]),
    ],
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
        ),
    ],
)

# Global key bindings.
bind.add("tab")(focus.next)
bind.add("s-tab")(focus.previous)


style = Style.add(
    {
        "window.border": "#888888",
        "shadow": "bg:#222222",
        "menu-bar": "bg:#aaaaaa #888888",
        "menu-bar.selected-item": "bg:#ffffff #000000",
        "menu": "bg:#888888 #ffffff",
        "menu.border": "#aaaaaa",
        "window.border shadow": "#444444",
        "focused  button": "bg:#880000 #ffffff noinherit",
        # Styling for Dialog widgets.
        "button-bar": "bg:#aaaaff",
    }
)


def main():
    container(
            content, 
            bind=True,
            focused_element=yes_button,
            full_screen=True,
            mouse_support=True,
            style=style
            )

if __name__ == "__main__":
    main()
