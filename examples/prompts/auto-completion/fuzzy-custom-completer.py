#!/usr/bin/env python
"""
Demonstration of a custom completer wrapped in a `FuzzyCompleter

"""
import quo

session = quo.Prompt()

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


class ColorCompleter(quo.completion.Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for color in colors:
            if color.startswith(word):
                yield quo.completion.Completion(
                    color,
                    start_position=-len(word),
                    style="fg:" + color,
                    selected_style="fg:white bg:" + color,
                )


def main():
    # Simple completion menu.
    print("(The completion menu displays colors.)")
    session.prompt("Type a color: ", completer=quo.completion.FuzzyCompleter(ColorCompleter()))

    # Multi-column menu.
    session.prompt(
        "Type a color: ",
        completer=quo.completion.FuzzyCompleter(ColorCompleter()),
        complete_style=quo.completion.CompleteStyle.multi_column,
    )

    # Readline-like
    session.prompt(
        "Type a color: ",
        completer=quo.completion.FuzzyCompleter(ColorCompleter()),
        complete_style=quo.completion.CompleteStyle.neat,
    )


if __name__ == "__main__":
    main()
