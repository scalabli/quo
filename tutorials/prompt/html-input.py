#!/usr/bin/env python
"""
Simple example of a syntax-highlighted HTML input line.
(This requires Pygments to be installed.)
"""
from pygments.lexers.html import HtmlLexer

from quo import echo, Elicit
from quo.lexers import PygmentsLexer


def main():
    s = Elicit()
    
    prompt = s.elicit("Enter HTML: ", lexer=PygmentsLexer(HtmlLexer))
    echo(f"You said:{prompt}")


if __name__ == "__main__":
    main()
