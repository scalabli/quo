#!/usr/bin/env python
"""
Autocompletion example that displays the autocompletions like readline does by
binding a custom handler to the Tab key.
"""
from quo.completion import WordCompleter
from quo.completion.core import CompleteStyle
from quo.prompt import Prompt

words = WordCompleter(
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
    ]
    )

session = Prompt(
        completer=words,
        complete_style=CompleteStyle.single_column
        )

def main():
    text = session.prompt("Give some animals: ")
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
