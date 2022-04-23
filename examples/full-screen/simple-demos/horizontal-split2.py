from quo import container
from quo.layout import HSplit, Window
from quo.widget import Label

# 1. The layout

content = HSplit([
    Label("\n\n(Top pane)"),
    Window(height=1, char="-"),  # Horizontal line in the middle.
    Label("\n\n(Bottom pane)")
    ])
# 2. The `Application`
container(content, bind=True)
