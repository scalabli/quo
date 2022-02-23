#!/usr/bin/env python
"""
A simple example of a scrollable pane.
"""

import quo

from quo.console import Console, get_app

def main():
    # Create a big layout of many text areas, then wrap them in a `ScrollablePane`.
    root_container = quo.widget.Frame(
        quo.layout.ScrollablePane(
            quo.layout.HSplit(
                [
                    quo.widget.Frame(quo.widget.TextArea(text=f"label-{i}"), width=quo.layout.Dimension())
                    for i in range(20)
                ]
            )
        ),
         quo.layout.ScrollablePane(quo.layout.HSplit([quo.widget.TextArea(text=f"label-{i}") for i in range(20)]))
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
    Console(
            layout=layout,
            bind=kb, 
            full_screen=True).run()


if __name__ == "__main__":
    main()
