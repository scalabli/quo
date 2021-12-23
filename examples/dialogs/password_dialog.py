#!/usr/bin/env python
"""
Example of an password input dialog.
"""
from quo.shortcuts import evoke


def main():
    result = evoke(
        title="Password dialog example",
        text="Please type your password:",
        password=True,
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
