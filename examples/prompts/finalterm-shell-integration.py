#!/usr/bin/env python
"""
Mark the start and end of the prompt with Final term (iterm2) escape sequences.
See: https://iterm2.com/finalterm.html
"""
import sys
from quo.prompt import Prompt
from quo.text import ANSI

session = Prompt()


BEFORE_PROMPT = "\033]133;A\a"
AFTER_PROMPT = "\033]133;B\a"
BEFORE_OUTPUT = "\033]133;C\a"
AFTER_OUTPUT = (
    "\033]133;D;{command_status}\a"  # command_status is the command status, 0-255
)


def get_prompt_text():
    # Generate the text fragments for the prompt.
    # Important: use the `ZeroWidthEscape` fragment only if you are sure that
    #            writing this as raw text to the output will not introduce any
    #            cursor movements.
    return [
        ("[ZeroWidthEscape]", BEFORE_PROMPT),
        ("", "Say something: # "),
        ("[ZeroWidthEscape]", AFTER_PROMPT),
    ]


if __name__ == "__main__":
    # Option 1: Using a `get_prompt_text` function:
    answer = session.prompt(get_prompt_text)

    # Option 2: Using ANSI escape sequences.
    before = "\001" + BEFORE_PROMPT + "\002"
    after = "\001" + AFTER_PROMPT + "\002"
    answer = session.prompt(ANSI("{}Say something: # {}".format(before, after)))

    # Output.
    sys.stdout.write(BEFORE_OUTPUT)
    print("You said: %s" % answer)
    sys.stdout.write(AFTER_OUTPUT.format(command_status=0))
