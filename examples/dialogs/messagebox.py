#!/usr/bin/env python
"""
Example of a message box window.
"""
import quo

def main():
    quo.MessageBox(
        title="Message pop up window",
        text="Do you want to continue?\nPress ENTER to quit.",
    ).run()


if __name__ == "__main__":
    main()
