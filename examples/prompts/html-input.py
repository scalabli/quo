#!/usr/bin/env python

from quo import echo
from quo.lexers import HtmlLexer
from quo.prompt import Prompt

session = Prompt()

def main():
    """Simple example of a syntax-highlighted HTML input line."""
    text = session.prompt("Enter HTML: ", lexer=HtmlLexer)
    echo(f"You said: {text}")


if __name__ == "__main__":
    main()
