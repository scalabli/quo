#!/usr/bin/env python
"""
Similar to the autocompletion example. But display all the completions in multiple columns.
"""

from quo.completion import WordCompleter
from quo.prompt import Prompt

session = Prompt()

animal_completer = WordCompleter(
    [
        "alligator",
        "ant",
        "ape",
        "bat",
        "bear",
        "beaver",
        "bee",
        "bison",
        "butterfly",
        "cat",
        "chicken",
        "crocodile",
        "dinosaur",
        "dog",
        "dolphin",
        "dove",
        "duck",
        "eagle",
        "elephant",
        "fish",
        "goat",
        "gorilla",
        "kangaroo",
        "leopard",
        "lion",
        "mouse",
        "rabbit",
        "rat",
        "snake",
        "spider",
        "turkey",
        "turtle",
    ],
    ignore_case=True,
)


def main():
    text = session.prompt(
        "Give some animals: ",
        completer=animal_completer,
        complete_style="multi_column"
        )
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
