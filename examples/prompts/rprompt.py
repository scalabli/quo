#!/usr/bin/env python
"""
Example of a right prompt. This is an additional prompt that is displayed on
the right side of the terminal. It will be hidden automatically when the input
is long enough to cover the right side of the terminal.

This is similar to RPROMPT is Zsh.
"""
import quo

session = quo.Prompt()

example_style = quo.styles.Style.add(
    {
        "rprompt": "bg:#ff0066 #ffffff",
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
    answer = session.prompt("> ", rprompt=" <Quo> ", style=example_style)
    print("You said: %s" % answer)

    # Option 2: pass HTML:
    answer = session.prompt("> ", rprompt=quo.text.HTML(" <u><bold>prompt</bold></u> "), style=example_style)
    print("You said: %s" % answer)

    # Option 3: Pass a callable. (This callable can either return plain text,
    #           an HTML object, or a list of (style, text)
    #           tuples.
    answer = session.prompt("> ", rprompt=get_rprompt_text, style=example_style)
    print("You said: %s" % answer)


if __name__ == "__main__":
    main()
