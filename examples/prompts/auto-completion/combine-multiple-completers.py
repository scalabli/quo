#!/usr/bin/env python
"""
Example of multiple individual completers that are combined into one.
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

color_completer = quo.completion.WordCompleter(
    [
        "red",
        "green",
        "blue",
        "yellow",
        "white",
        "black",
        "orange",
        "gray",
        "pink",
        "purple",
        "cyan",
        "magenta",
        "violet",
    ],
    ignore_case=True,
)


def main():
    completer = quo.completion.merge_completers([animal_completer, color_completer])

    text = session.prompt(
        "Give some animals: ", completer=completer, complete_while_typing=False
    )
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
