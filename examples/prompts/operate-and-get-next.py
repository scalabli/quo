#!/usr/bin/env python
"""
Demo of "operate-and-get-next".

(Actually, this creates one prompt application, and keeps running the same app
over and over again. -- For now, this is the only way to get this working.)
"""

import quo


def main():
    session = quo.Prompt("prompt> ")
    while True:
        session.prompt()


if __name__ == "__main__":
    main()
