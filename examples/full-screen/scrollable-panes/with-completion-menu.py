#!/usr/bin/env python
"""
A simple example of a scrollable pane.
"""

import quo

from quo.suite.current import get_app
from quo.completion import WordCompleter


def main():
    # Create a big layout of many text areas, then wrap them in a `ScrollablePane`.
    root_container = quo.layout.VSplit(
        [
            quo.widgets.Label("<left column>"),
            quo.layout.HSplit(
                [
                    quo.widgets.Label("ScrollContainer Demo"),
                    quo.widgets.Frame(
                        quo.layout.ScrollablePane(
                            quo.layout.HSplit(
                                [
                                    quo.widgets.Frame(
                                        quo.widgets.TextArea(
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

    root_container = quo.layout.FloatContainer(
        root_container,
        floats=[
            quo.layout.Float(
                xcursor=True,
                ycursor=True,
                content=quo.layout.CompletionsMenu(max_height=16, scroll_offset=1),
            ),
        ],
    )

    layout = quo.layout.Layout(container=root_container)

    # Key bindings.
    kb = quo.keys.KeyBinder()

    @kb.add("ctrl-c")
    def exit(event) -> None:
        get_app().exit()

    kb.add("tab")(quo.keys.focus.next)
    kb.add("s-tab")(quo.keys.focus.previous)

    # Create and run application.
    application = quo.Suite(
            layout=layout, 
            bind=kb, 
            full_screen=True,
            mouse_support=True
    )
    application.run()


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
