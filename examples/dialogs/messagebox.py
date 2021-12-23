#!/usr/bin/env python
"""
Example of a message box window.
"""
from quo.shortcuts import message

def main():
    message(
        title="Example dialog window",
        text="Do you want to continue?\nPress ENTER to quit.",
    ).run()


if __name__ == "__main__":
    main()
