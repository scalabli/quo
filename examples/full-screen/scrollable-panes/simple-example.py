#!/usr/bin/env python
"""
A simple example of a scrollable pane.
"""

import quo

from quo.suite.current import get_app

from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import Dimension, HSplit, Layout, ScrollablePane
from prompt_toolkit.widgets import Frame, Label, TextArea


def main():
    # Create a big layout of many text areas, then wrap them in a `ScrollablePane`.
    root_container = quo.widgets.Frame(
        quo.layout.ScrollablePane(
            HSplit(
                [
                    quo.widgets.Frame(quo.widgets.TextArea(text=f"label-{i}"), width=Dimension())
                    for i in range(20)
                ]
            )
        )
        # ScrollablePane(HSplit([TextArea(text=f"label-{i}") for i in range(20)]))
    )

    layout = quo.layout.Layout(container=root_container)

    # Key bindings.
    kb = quo.keys.KeyBinder()

    @kb.add("ctrl-c")
    def exit(event) -> None:
        get_app().exit()

    kb.add("tab")(focus_next)
    kb.add("s-tab")(focus_previous)

    # Create and run application.
    application = quo.Suite(layout=layout, key_bindings=kb, full_screen=True)
    application.run()


if __name__ == "__main__":
    main()
