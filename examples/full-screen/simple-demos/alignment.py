#!/usr/bin/env python
"""
Demo of the different Window alignment options.
"""

import quo

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

hsplit = quo.layout.HSplit
window = quo.layout.Window
windowalign = quo.layout.WindowAlign
formattedtextcontrol = quo.layout.FormattedTextControl
body = hsplit(
    [
        window(formattedtextcontrol(left_text), align=windowalign.LEFT),
        window(height=1, char="-"),
        window(formattedtextcontrol(center_text), align=windowalign.CENTER),
        window(height=1, char="-"),
        window(formattedtextcontrol(right_text), align=windowalign.RIGHT),
    ]
)


# 2. Key bindings
kb = quo.keys.KeyBinder()


@kb.add("q")
def _(event):
    "Quit application."
    event.app.exit()

layout = quo.layout.Layout

# 3. The `Console` app
application = quo.Console(layout=layout(body), bind=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
