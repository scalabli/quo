#!/usr/bin/env python
"""
Example usage of 'container', a tool to print
any layout in a non-interactive way.
"""
import quo

from quo.shortcuts import container

container(
    quo.widgets.Frame(
        quo.widgets.TextArea(text="Hello world!\n"),
        title="Stage: parse",
    )
)
