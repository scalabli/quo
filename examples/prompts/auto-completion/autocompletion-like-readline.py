#!/usr/bin/env python
"""
Autocompletion example that displays the autocompletions like readline does by
binding a custom handler to the Tab key.
"""
import quo

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

session = quo.Prompt()
def main():
    text = session.prompt(
        "Give some animals: ",
        completer=animal_completer,
        complete_style=quo.completion.CompleteStyle.neat)
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
