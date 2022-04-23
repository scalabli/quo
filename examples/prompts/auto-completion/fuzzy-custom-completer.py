#!/usr/bin/env python
"""
Demonstration of a custom completer wrapped in a `FuzzyCompleter

"""

from quo.completion import Completer, Completion, FuzzyCompleter
from quo.prompt import Prompt


colors = [
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "yellow",
    "cyan",
    "magenta",
    "pink",
]


class ColorCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for color in colors:
            if color.startswith(word):
                yield Completion(
                    color,
                    start_position=-len(word),
                    style="fg:" + color,
                    selected_style="fg:white bg:" + color)



session = Prompt()

def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")
    session.prompt("Type a color: ", completer=FuzzyCompleter(ColorCompleter()))

    # Multi-column menu.
    session.prompt(
        "Type a color: ",
        completer=FuzzyCompleter(ColorCompleter()),
        complete_style="multi_column"
    )

    # Readline-like
    session.prompt(
        "Type a color: ",
        completer=FuzzyCompleter(ColorCompleter()),
        complete_style="readline"
    )


if __name__ == "__main__":
    main()
