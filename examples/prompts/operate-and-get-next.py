#!/usr/bin/env python
"""
Demo of "operate-and-get-next".

(This creates one prompt application that keeps running over and over again.)
"""
from quo.shortcuts import Elicit


def main():
    session = Elicit("Type anything:> ")
    while True:
        session.elicit()


if __name__ == "__main__":
    main()
