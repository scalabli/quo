#!/usr/bin/env python3

from quo import echo
from quo.prompt import Prompt
from quo.text import Text

session = Prompt()

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
        return Text("<strong>%s</strong>") % text


session = Prompt(multiline=True, prompt_continuation=prompt_continuation)
if __name__ == "__main__":
    echo("Press [Meta+Enter] or [Esc] followed by [Enter] to accept input.")
    answer = session.prompt("Multiline input: ")
    print("You said: %s" % answer)
