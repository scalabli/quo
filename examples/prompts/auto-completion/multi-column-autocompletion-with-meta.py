#!/usr/bin/env python
"""
Autocompletion example that shows meta-information alongside the completions.
"""

from quo.completion import WordCompleter
from quo.prompt import Prompt


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
    ],
    meta_dict={
        "alligator": "An alligator is a crocodilian in the genus Alligator of the family Alligatoridae.",
        "ant": "Ants are eusocial insects of the family Formicidae",
        "ape": "Apes (Hominoidea) are a branch of Old World tailless anthropoid catarrhine primates ",
        "bat": "Bats are mammals of the order Chiroptera",
    }
)


session = Prompt(
        completer=animal_completer,
        complete_style="multi_column"
        )
def main():
    text = session.prompt("Give some animals: ")
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
