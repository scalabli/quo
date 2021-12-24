#!/usr/bin/env python

from pygments.lexers.html import HtmlLexer

import quo

session = quo.Prompt()

@quo.command()
@quo.app("@lexer", help="This requires Pygments to be installed")
def main(lexer):
    """Simple example of a syntax-highlighted HTML input line."""
    text = session.prompt("Enter HTML: ", lexer=quo.lexers.PygmentsLexer(HtmlLexer))
    quo.echo(f"You said: {text}")


if __name__ == "__main__":
    main()
