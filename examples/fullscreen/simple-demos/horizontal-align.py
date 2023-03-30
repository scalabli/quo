"""
Horizontal align demo with HSplit.
"""
from quo.layout import HSplit, VSplit, FormattedTextControl
from quo.layout.dimension import D
from quo.layout.layout import Layout
from quo.widget import Frame, Box, Label
from quo.bar import Bar

from quo import container
from quo.keys import bind
from quo.label import Label
from quo.window import Window


TITLE = """ <u><cyan>HSplit and VSplit</cyan></u> demo.
 Press <b>'q'</b> to quit."""

LIPSUM = """\
Lorem ipsum dolor
sit amet, consectetur
adipiscing elit.
Maecenas quis
interdum enim."""

label = Label(TITLE)
window = Window(label)
box = Box(window)
frame = Frame(box, height=4)

body = HSplit(
    [
        frame,

        HSplit(
            [
                # Left alignment.
                VSplit(
                    [
                        Window(
                            Label("<u><blue>LEFT</blue></u>"),
                            width=10,
                            ignore_content_width=True,
                            style="bg:#ff3333 ansiblack",
                            align="center"
                        ),
                        VSplit(
                            [
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                            ],
                            padding=1,
                            padding_style="bg:#888888",
                            align="left",
                            height=5,
                            padding_char="|",
                        ),
                    ]
                ),
                # Center alignment.
                VSplit(
                    [
                        Window(
                            Label("<u><green>CENTER</green></u>"),
                            width=10,
                            ignore_content_width=True,
                            style="bg:#ff3333 ansiblack",
                            align="center"
                        ),
                        VSplit(
                            [
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                            ],
                            padding=1,
                            padding_style="bg:#888888",
                            align="center",
                            height=5,
                            padding_char="|",
                        ),
                    ]
                ),
                # Right alignment.
                VSplit(
                    [
                        Window(
                            FormattedTextControl("<u>RIGHT</u>"),
                            width=10,
                            ignore_content_width=True,
                            style="bg:#ff3333 ansiblack",
                            align="center"
                        ),
                        VSplit(
                            [
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM),
                                    height=4,
                                    style="bg:#444488",
                                ),
                            ],
                            padding=1,
                            padding_style="bg:#888888",
                            align="right",
                            height=5,
                            padding_char="|",
                        ),
                    ]
                ),
                # Justify
                VSplit(
                    [
                        Window(
                            FormattedTextControl("<u>JUSTIFY</u>"),
                            width=10,
                            ignore_content_width=True,
                            style="bg:#ff3333 ansiblack",
                            align="center"
                        ),
                        VSplit(
                            [
                                Window(
                                    FormattedTextControl(LIPSUM), style="bg:#444488"
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM), style="bg:#444488"
                                ),
                                Window(
                                    FormattedTextControl(LIPSUM), style="bg:#444488"
                                ),
                            ],
                            padding=1,
                            padding_style="bg:#888888",
                            align="justify",
                            height=5,
                            padding_char="|",
                        ),
                    ]
                ),
            ],
            padding=1,
            padding_style="bg:#ff3333 #ffffff",
            padding_char=".",
            align="top"
        ),
    ]
)


# 2. Key bindings
@bind.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`


container(body, bind=True, full_screen=True)
