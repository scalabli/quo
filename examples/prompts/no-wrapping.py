#!/usr/bin/env python3

import quo

session = quo.Prompt()

if __name__ == "__main__":
    answer = session.prompt("Give me some input: ", wrap_lines=False, multiline=True)
    quo.echo(f"You said: {answer}")
