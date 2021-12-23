#!/usr/bin/env python
"""
Simple example of a syntax-highlighted HTML input line.
(This requires Pygments to be installed.)
"""
from pygments.lexers.html import HtmlLexer

import quo

session = quo.Prompt()

def main():
    text = session.prompt("Enter HTML: ", lexer=quo.lexers.PygmentsLexer(HtmlLexer))
    quo.echo(f"You said: {text}")


if __name__ == "__main__":
    main()
