import quo

from quo.layout.controls import BufferControl, FormattedTextControl

# 1. The layout
top_text = (
    "Focus example.\n"
    "[q] Quit [a] Focus left top [b] Right top [c] Left bottom [d] Right bottom."
)

content = """
placerat massa tempor elementum. Sed tristique mauris ac
tempus vehicula augue non venenatis. Mauris aliquam velit turpis, nec congue
risus aliquam sit amet. Pellentesque blandit scelerisque felis, faucibus
consequat ante. Curabitur tempor tortor a imperdiet tincidunt. Nam sed justo
sit amet odio bibendum congue. Quisque varius ligu
Quo is a Python based toolkit for writing Command-Line Interface(CLI) applications. Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API. Simple to code, easy to learn, and does not come with needless baggage. """


left_top = quo.layout.Window(BufferControl(quo.buffer.Buffer(document=quo.document.Document(content))))
left_bottom = quo.layout.Window(BufferControl(quo.buffer.Buffer(document=quo.document.Document(content))))
right_top = quo.layout.Window(BufferControl(quo.buffer.Buffer(document=quo.document.Document(content))))
right_bottom = quo.layout.Window(BufferControl(quo.buffer.Buffer(document=quo.document.Document(content))))


body = quo.layout.HSplit(
    [
        quo.layout.Window(FormattedTextControl(top_text), height=2, style="reverse"),
        quo.layout.Window(height=1, char="-"),  # Horizontal line in the middle.
        quo.layout.VSplit([left_top, quo.layout.Window(width=1, char="|"), right_top]),
        quo.layout.Window(height=1, char="-"),  # Horizontal line in the middle.
        quo.layout.VSplit([left_bottom, quo.layout.Window(width=1, char="|"), right_bottom]),
    ]
)


# 2. Key bindings
kb = quo.keys.KeyBinder()


@kb.add("q")
def _(event):
    "Quit application."
    event.app.exit()


@kb.add("a")
def _(event):
    event.app.layout.focus(left_top)


@kb.add("b")
def _(event):
    event.app.layout.focus(right_top)


@kb.add("c")
def _(event):
    event.app.layout.focus(left_bottom)


@kb.add("d")
def _(event):
    event.app.layout.focus(right_bottom)


@kb.add("tab")
def _(event):
    event.app.layout.focus_next()


@kb.add("s-tab")
def _(event):
    event.app.layout.focus_previous()


# 3. The `Application`
application = quo.Suite(layout=quo.layout.Layout(body), key_bindings=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
