"""
This example demonstrates a simple text highlighter.
"""

from quo.console import Console
from quo.highlight import RegexHighlighter
from quo.theme import Theme


class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)

console.evoke("Send funds to money@example.org")
