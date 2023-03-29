#!/usr/bin/env python
"""
Demo of the different Window alignment options.
"""
from quo import container
from quo.layout import FormattedTextControl, HSplit, Window

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

left_text = '\nLeft aligned text. - (Press `ctrl-c` to quit)\n\n' + LIPSUM
center_text = "Centered text.\n\n" + LIPSUM
right_text = "Right aligned text.\n\n" + LIPSUM

content = HSplit(
    [
        Window(FormattedTextControl(left_text), align="left"),
        Window(height=3, char="-"),
        Window(FormattedTextControl(center_text), align="center"),
        Window(height=1, char="-"),
        Window(FormattedTextControl(right_text), align="right")
    ]
)



# 3. The `Application`

container(content, bind=True, full_screen=True)


