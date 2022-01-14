#!/usr/bin/env python
"""
Similar to the autocompletion example. But display all the completions in multiple columns.
"""
import quo

session = quo.Prompt()

animal_completer = quo.completion.WordCompleter(
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
        complete_style=quo.completion.CompleteStyle.multi_column,
    )
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
