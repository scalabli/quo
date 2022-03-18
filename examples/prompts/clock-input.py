#!/usr/bin/env python
"""
Example of a 'dynamic' prompt. On that shows the current time in the prompt.
"""
import datetime

from quo import echo
from quo.prompt import Prompt
from quo.style import Style

style = Style.add({'':'fg:red'})

def get_prompt():
    "Tokens to be shown before the prompt."
    now = datetime.datetime.now()
    return [
            ("bg:green fg:black", "%s:%s:%s"  % (now.hour, now.minute, now.second)),
            ("bg:cornsilk fg:maroon", "Enter something: ")
    ]

session = Prompt(refresh_interval=0.5)#, style="style")
def main():
    result = session.prompt(get_prompt)
    echo(f"You said: {result}")


if __name__ == "__main__":
    main()
