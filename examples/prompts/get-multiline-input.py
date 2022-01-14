#!/usr/bin/env python3

import quo

session = quo.Prompt()

def prompt_continuation(width, line_number, wrap_count):
    """
    The continuation: display line numbers and '->' before soft wraps.

    Notice that we can return any kind of formatted text from here.

    The prompt continuation doesn't have to be the same width as the prompt
    which is displayed before the first line, but in this example we choose to
    align them. The `width` input that we receive here represents the width of
    the prompt.
    """
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = ("- %i - " % (line_number + 1)).rjust(width)
        return quo.text.HTML("<strong>%s</strong>") % text


if __name__ == "__main__":
    quo.echo("Press [Meta+Enter] or [Esc] followed by [Enter] to accept input.")
    answer = session.prompt(
        "Multiline input: ", multiline=True, elicit_continuation=prompt_continuation
    )
    print("You said: %s" % answer)
