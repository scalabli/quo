#!/usr/bin/env python
"""
Example of confirmation (yes/no) dialog window.
"""
from quo.shortcuts import confirmation

def main():
    result = confirmation(
        title="Yes/No dialog example", text="Do you want to confirm?"
    ).run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
