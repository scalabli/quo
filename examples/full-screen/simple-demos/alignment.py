#!/usr/bin/env python
"""
Demo of the different Window alignment options.
"""
from quo.console import Console
from quo.keys import Bind
from quo.layout import Layout, FormattedTextControl, HSplit, Window
from quo.text import Text


LIPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Maecenas
quis interdum enim. Nam viverra, mauris et blandit malesuada, ante est bibendum
mauris, ac dignissim dui tellus quis ligula. Aenean condimentum leo at
dignissim placerat. In vel dictum ex, vulputate accumsan mi. Donec ut quam
placerat massa tempor elementum. Sed tristique mauris ac suscipit euismod. Ut
tempus vehicula augue non venenatis. Mauris aliquam velit turpis, nec congue
risus aliquam sit amet. Pellentesque blandit scelerisque felis, faucibus
consequat ante. Curabitur tempor tortor a imperdiet tincidunt. Nam sed justo
sit amet odio bibendum congue. Quisque varius ligula nec ligula gravida, sed
convallis augue faucibus. Nunc ornare pharetra bibendum. Praesent blandit ex
quis sodales maximus."""

# 1. The layout

left_text = '\nLeft aligned text. - (Press "q" to quit)\n\n' + LIPSUM
center_text = "Centered text.\n\n" + LIPSUM
right_text = "Right aligned text.\n\n" + LIPSUM

body = HSplit(
    [
        Window(FormattedTextControl(left_text), align="left"),
        Window(height=1, char="-"),
        Window(FormattedTextControl(center_text), align="center"),
        Window(height=1, char="-"),
        Window(FormattedTextControl(right_text), align="right")
    ]
)


# 2. Key bindings
kb = Bind()


@kb.add("q")
def _(event):
    "Quit application."
    event.app.exit()

# 3. The `Console` app
application = Console(layout=Layout(body), bind=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
