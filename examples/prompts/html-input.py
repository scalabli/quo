#!/usr/bin/env python

from quo import echo
from quo.highlight import HTML
from quo.prompt import Prompt

session = Prompt(highlighter=HTML)

def main():
    """Simple example of a syntax-highlighted HTML input line."""
    text = session.prompt("Enter HTML: ")
    echo(f"You said: {text}")


if __name__ == "__main__":
    main()
