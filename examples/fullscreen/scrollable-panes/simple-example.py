#!/usr/bin/env python
"""
A simple example of a scrollable pane.
"""


from quo import container
from quo.console import get_app
from quo.keys import bind, focus
from quo.layout import Dimension, HSplit, ScrollablePane
from quo.widget import Frame, TextArea

def main():
    # Create a big layout of many text areas, then wrap them in a `ScrollablePane`.
    content = Frame(
        ScrollablePane(
            HSplit(
                [
                    Frame(TextArea(text=f"label-{i}"), width=Dimension())
                    for i in range(20)
                ]
            )
        ),
         ScrollablePane(
             HSplit([
                 TextArea(text=f"label-{i}") for i in range(20)]))
    )

    #layout = quo.layout.Layout(container=root_container)

    # Key bindings.

    @bind.add("ctrl-c")
    def exit(event) -> None:
        get_app().exit()

    bind.add("tab")(focus.next)
    bind.add("s-tab")(focus.previous)

    # Create and run application.
    container(
            content, bind=True, full_screen=True)
if __name__ == "__main__":
    main()
