#!/usr/bin/env python
"""
Example usage of 'container', a tool to print
any layout in a non-interactive way.
"""
from quo import container
from quo.widget import Frame, TextArea

def main():
    """ Example of a simple layout"""

    content = TextArea(text="Hello world🌍")
    container(
            Frame(
                content,
                title="Quo: python🐍")
            )

if __name__ == "__main__":
    main()
