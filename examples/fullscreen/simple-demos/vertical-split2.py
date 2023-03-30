#!/usr/bin/env python
"""
Vertical split example.
"""
from quo import container
from quo.layout import VSplit, Window
from quo.widget import Label

# 1. The layout
content = VSplit([
    Label("(Left pane)"),
    Window(width=1, char="|", style="fg:green"),  # Vertical line in the middle.
    Label("(Right pane)")
    ])


container(content, bind=True, full_screen=True)


