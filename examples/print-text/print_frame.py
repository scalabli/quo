#!/usr/bin/env python
"""
Example usage of 'container', a tool to print
any layout in a non-interactive way.
"""
from quo import container
from quo.widget import Frame, TextArea

def main():
    """ Example of a simple layout"""

    content = Frame(
                TextArea("Hello world!"),
                title="Quo: python🐍")

    container(content, bind=False)

if __name__ == "__main__":
    main()
