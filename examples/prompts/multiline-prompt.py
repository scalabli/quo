#!/usr/bin/env python
"""
Demonstration of how the input can be indented.
"""
import quo

session = quo.Prompt()

if __name__ == "__main__":
    answer = session.prompt(
        "Give me some input: (ESCAPE followed by ENTER to accept)\n > ", multiline=True
    )
    quo.echo(f"You said: {answer}")
