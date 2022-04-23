#!/usr/bin/env python
"""
Demonstration of a custom completer class and the possibility of styling
completions independently.
"""
from quo.completion import Completer, Completion
from quo.color import ColorDepth
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
                    selected_style="fg:white bg:" + color,
                )



def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")
    session = Prompt(completer=ColorCompleter())
    session.prompt("Type a color: ")

    # Multi-column menu.
    session = Prompt(completer=ColorCompleter(), complete_style="multi_column")
    session.prompt("Type a color: ")


    # Readline-like
    session = Prompt(completer=ColorCompleter(), complete_style="readline")
    session.prompt("Type a color: ")


    # Prompt with true color output.
    message = [
        ("#cc2244", "T"),
        ("#bb4444", "r"),
        ("#996644", "u"),
        ("#cc8844", "e "),
        ("#ccaa44", "C"),
        ("#bbaa44", "o"),
        ("#99aa44", "l"),
        ("#778844", "o"),
        ("#55aa44", "r "),
        ("#33aa44", "p"),
        ("#11aa44", "r"),
        ("#11aa66", "o"),
        ("#11aa88", "m"),
        ("#11aaaa", "p"),
        ("#11aacc", "t"),
        ("#11aaee", ": "),
    ]

    session = Prompt(completer=ColorCompleter(), color_depth="true_color")
    session.prompt(message)

if __name__ == "__main__":
    main()
