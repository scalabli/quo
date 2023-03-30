#!/usr/bin/env python
"""
Horizontal split example.
"""
from quo import container
from quo.layout import Float, FloatContainer, Window, FormattedTextControl
from quo.widget import Frame

LIPSUM = " ".join(
    (
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Maecenas quis interdum enim. Nam viverra, mauris et blandit malesuada, ante est
bibendum mauris, ac dignissim dui tellus quis ligula. Aenean condimentum leo at
dignissim placerat. In vel dictum ex, vulputate accumsan mi. Donec ut quam
placerat massa tempor elementum. Sed tristique mauris ac suscipit euismod. Ut
tempus vehicula augue non venenatis. Mauris aliquam velit turpis, nec congue
risus aliquam sit amet. Pellentesque blandit scelerisque felis, faucibus
consequat ante. Curabitur tempor tortor a imperdiet tincidunt. Nam sed justo
sit amet odio bibendum congue. Quisque varius ligula nec ligula gravida, sed
convallis augue faucibus. Nunc ornare pharetra bibendum. Praesent blandit ex
quis sodales maximus. """
        * 100
    ).split()
)


# 1. The layout
left_text = "Floating\nleft"
right_text = "Floating\nright"
top_text = "Floating\ntop"
bottom_text = "Floating\nbottom"
center_text = "Floating\ncenter"
quit_text = "Press 'q' to quit."


content = FloatContainer(
        Window(FormattedTextControl(LIPSUM), wrap_lines=True),
    floats=[
        # Important note: Wrapping the floating objects in a 'Frame' is
        #                 only required for drawing the border around the
        #                 floating text. We do it here to make the layout more
        #                 obvious.
        # Left float.
        Float(
            Frame(
                Window(FormattedTextControl(left_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            left=0,
        ),
        # Right float.
        Float(
            Frame(
                Window(FormattedTextControl(right_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            right=0,
        ),
        # Bottom float.
        Float(
            Frame(
                Window(FormattedTextControl(bottom_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            bottom=0,
        ),
        # Top float.
        Float(
            Frame(
                Window(FormattedTextControl(top_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            top=0,
        ),
        # Center float.
        Float(
            Frame(
                Window(FormattedTextControl(center_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            )
        ),
        # Quit text.
        Float(
            Frame(
                Window(FormattedTextControl(quit_text), width=18, height=1),
                style="bg:#ff44ff #ffffff",
            ),
            top=6,
        ),
    ],
)


# 3. The `Application`
container(content, bind=True, full_screen=True)


