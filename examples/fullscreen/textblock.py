from quo.layout import HSplit

from quo import container
#from quo.layout.containers import Window
from quo.window import Window
from quo.label import Label


# 1. The layout
left_text = "\nVertical-split example. Press 'q' to quit.\n\n(top pane.)"
right_text = "\n(bottom pane.)"


body = HSplit(
    [

        Window(Label(left_text), style="red")
      
        #Window(FormattedTextControl(left_text)),
        #Window(height=1, char="-"),  # Horizontal line in the middle.
        #Window(FormattedTextControl(right_text)),
    ]
)


container(body)