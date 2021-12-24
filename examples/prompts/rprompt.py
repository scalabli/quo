#!/usr/bin/env python
"""
Example of a right prompt. This is an additional prompt that is displayed on
the right side of the terminal. It will be hidden automatically when the input
is long enough to cover the right side of the terminal.

This is similar to RPROMPT is Zsh.
"""
import quo

session = quo.Prompt()

example_style = quo.styles.Style.from_dict(
    {
        "r_elicit": "bg:#ff0066 #ffffff",
    }
)


def get_rprompt_text():
    return [
        ("", " "),
        ("underline", "<r_elicit>"),
        ("", " "),
    ]


def main():
    # Option 1: pass a string to 'rprompt':
    answer = session.prompt("> ", r_elicit=" <r_elicit> ", style=example_style)
    print("You said: %s" % answer)

    # Option 2: pass HTML:
    answer = session.prompt("> ", r_elicit=quo.text.HTML(" <u>&lt;rprompt&gt;</u> "), style=example_style)
    print("You said: %s" % answer)

    # Option 3: pass ANSI:
    answer = session.prompt(
        "> ", r_elicit=quo.text.ANSI(" \x1b[4m<rprompt>\x1b[0m "), style=example_style
    )
    print("You said: %s" % answer)

    # Option 4: Pass a callable. (This callable can either return plain text,
    #           an HTML object, an ANSI object or a list of (style, text)
    #           tuples.
    answer = session.prompt("> ", r_elicit=get_rprompt_text, style=example_style)
    print("You said: %s" % answer)


if __name__ == "__main__":
    main()
