#!/usr/bin/env python3
"""
Example of a right prompt. This is an additional prompt that is displayed on
the right side of the terminal. It will be hidden automatically when the input
is long enough to cover the right side of the terminal.

This is similar to RPROMPT is Zsh.
"""
from quo import echo
from quo.text import Text
from quo.prompt import Prompt
from quo.style import Style

session = Prompt()

example = Style.add(
    {
        "rprompt": "bg:red fg:white",
    }
)


def get_rprompt_text():
    return [
        ("", " "),
        ("underline", "<rprompt>"),
        ("", " "),
    ]


def main():
    # Option 1: pass a string to 'rprompt':
    answer = session.prompt("> ", rprompt=" <Quo> ", style=example)
    echo("You said: %s" % answer)

    # Option 2: pass HTML:
    answer = session.prompt("> ", rprompt=Text(" <u><bold>prompt</bold></u> "), style=example)
    echo("You said: %s" % answer)

    # Option 3: Pass a callable. (This callable can either return plain text,
    #           an HTML object, or a list of (style, text)
    #           tuples.
    answer = session.prompt("> ", rprompt=get_rprompt_text, style=example)
    echo("You said: %s" % answer)


if __name__ == "__main__":
    main()
