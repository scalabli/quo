"""

This example demonstrates how to write a custom highlighter.

"""

from random import randint

from quo import Console
from quo.highlighter import Highlighter


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)
console = Console()

rainbow = RainbowHighlighter()
console.echo(rainbow("I must not fear. Fear is the mind-killer."))
