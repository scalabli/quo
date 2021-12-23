#!/usr/bin/env python
"""
Example of a placeholer that's displayed as long as no input is given.
"""
import quo

session = quo.Prompt(placeholder=quo.HTML('<style color="#888888">(please type something)</style>'))

if __name__ == "__main__":
    answer = session.prompt("")
    quo.echo(f"You said: {answer}")
