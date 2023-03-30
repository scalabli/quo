#!/usr/bin/env python
"""
A simple example of a scrollable pane.
"""
from quo import container
from quo.completion import WordCompleter
from quo.console import get_app
from quo.keys import bind, focus
from quo.layout import CompletionsMenu, Float, FloatContainer, HSplit, VSplit, ScrollablePane
from quo.widget import Frame, Label, TextArea

def main():
    # Create a big layout of many text areas, then wrap them in a `ScrollablePane`.
    content = VSplit(
        [
            Label("<left column>"),
            HSplit(
                [
                    Label("ScrollContainer Demo"),
                    Frame(
                        ScrollablePane(
                            HSplit(
                                [
                                    Frame(
                                        TextArea(
                                            text=f"label-{i}",
                                            completer=animal_completer,
                                        )
                                    )
                                    for i in range(20)
                                ]
                            )
                        ),
                    ),
                ]
            ),
        ]
    )

    root_container = FloatContainer(
        content,
        floats=[
            Float(
                xcursor=True,
                ycursor=True,
                content=CompletionsMenu(max_height=16, scroll_offset=1),
            ),
        ],
    )

    # Key bindings.
    @bind.add("ctrl-c")
    def exit(event) -> None:
        get_app().exit()

    bind.add("tab")(focus.next)
    bind.add("s-tab")(focus.previous)

    # Create and run application.
    container(root_container, bind=True, full_screen=True, mouse_support=True)
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


if __name__ == "__main__":
    main()
