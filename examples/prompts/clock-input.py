#!/usr/bin/env python
"""
Example of a 'dynamic' prompt. On that shows the current time in the prompt.
"""
import datetime

import quo

console = quo.Prompt()

def get_prompt():
    "Tokens to be shown before the prompt."
    now = datetime.datetime.now()
    return [
        ("bg:#008800 #ffffff", "%s:%s:%s" % (now.hour, now.minute, now.second)),
        ("bg:cornsilk fg:maroon", " Enter something: "),
    ]


def main():
    result = console.prompt(get_prompt, refresh_interval=0.5)
    quo.echo(f"You said: {result}")


if __name__ == "__main__":
    main()
