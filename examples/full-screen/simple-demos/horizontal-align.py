"""
Horizontal align demo with HSplit.
"""
from quo.console import Console
from quo.keys import Bind
from quo.layout import HSplit, VSplit,   Window, FormattedTextControl
from quo.layout.dimension import D
from quo.layout.layout import Layout
from quo.text import Text
from quo.widget import Frame, Box

TITLE = Text(
    """ <u>HSplit HorizontalAlign</u> example.
 Press <b>'q'</b> to quit."""
)

LIPSUM = """\
Lorem ipsum dolor
sit amet, consectetur
adipiscing elit.
Maecenas quis
interdum enim."""


# 1. The layout
body = HSplit(
    [
        Frame(
            Box(
            Window(FormattedTextControl(TITLE),align="center", style="bg:#88ff88 #000000"), style="fg:red")
        ),
        HSplit(
            [
                # Left alignment.
                VSplit(
                    [
                        Window(
                            FormattedTextControl(Text("<u>LEFT</u>")),
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
                            FormattedTextControl(Text("<u>CENTER</u>")),
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
                            FormattedTextControl(Text("<u>RIGHT</u>")),
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
                            FormattedTextControl(Text("<u>JUSTIFY</u>")),
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
bind = Bind()

@bind.add("q")
def _(event):
    "Quit application."
    event.app.exit()


# 3. The `Application`
application = Console(layout=Layout(body), bind=bind,full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
