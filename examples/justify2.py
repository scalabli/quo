"""
This example demonstrates the justify argument to print.
"""

from quo import Console
from quo.panel import Panel
fg or bg = style
console = Console(width=20, height=49)

style = "blue"
panel = Panel("Quo", fg="on red", expand=False)
console.echo(panel, style=style)
console.echo(panel, style=style, justify="left")
console.echo(panel, style=style, justify="center")
console.echo(panel, style=style, justify="right")
