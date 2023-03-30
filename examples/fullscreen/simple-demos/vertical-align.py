#!/usr/bin/env python
"""
Vertical align demo with VSplit.
"""
from quo import container
from quo.keys import bind
from quo.text import Text
from quo.layout import (
    HSplit,
    VSplit,
    Window
)
from quo.layout import FormattedTextControl
from quo.layout import Dimension as D
from quo.layout import Layout
from quo.widget import Frame

TITLE = Text(
    """ <u>VSplit VerticalAlign</u> example.
 Press <b>'q'</b> to quit."""
)

LIPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Maecenas
quis interdum enim. Nam viverra, mauris et blandit malesuada, ante est bibendum
mauris, ac dignissim dui tellus quis ligula. Aenean condimentum leo at
dignissim placerat."""

content = HSplit(
    [
        Frame(
            Window(FormattedTextControl(TITLE), height=2), style="bg:#88ff88 #000000"
        ),
        VSplit(
            [
                Window(
                    FormattedTextControl(Text("  <u>VerticalAlign.TOP</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#ff3333 #000000 bold",
                    align="center",
                ),
                Window(
                    FormattedTextControl(Text("  <u>VerticalAlign.CENTER</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#ff3333 #000000 bold",
                    align="center",
                ),
                Window(
                    FormattedTextControl(Text("  <u>VerticalAlign.BOTTOM</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#ff3333 #000000 bold",
                    align="center",
                ),
                Window(
                    FormattedTextControl(Text("  <u>VerticalAlign.JUSTIFY</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#ff3333 #000000 bold",
                    align="center",
                ),
            ],
            height=1,
            padding=1,
            padding_style="bg:#ff3333",
        ),
        VSplit(
            [
                # Top alignment.
                HSplit(
                    [
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                    ],
                    padding=1,
                    padding_style="bg:#888888",
                    align="top",
                    padding_char="~",
                ),
                # Center alignment.
                HSplit(
                    [
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                    ],
                    padding=1,
                    padding_style="bg:#888888",
                    align="center",
                    padding_char="~",
                ),
                # Bottom alignment.
                HSplit(
                    [
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                        Window(
                            FormattedTextControl(LIPSUM), height=4, style="bg:#444488"
                        ),
                    ],
                    padding=1,
                    padding_style="bg:#888888",
                    align="bottom",
                    padding_char="~",
                ),
                # Justify
                HSplit(
                    [
                        Window(FormattedTextControl(LIPSUM), style="bg:#444488"),
                        Window(FormattedTextControl(LIPSUM), style="bg:#444488"),
                        Window(FormattedTextControl(LIPSUM), style="bg:#444488"),
                    ],
                    padding=1,
                    padding_style="bg:#888888",
                    align="justify",
                    padding_char="~",
                ),
            ],
            padding=1,
            padding_style="bg:#ff3333 #ffffff",
            padding_char=".",
        ),
    ]
)


# 2. Key bindings
@bind.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`

container(content, bind=True, full_screen=True)

