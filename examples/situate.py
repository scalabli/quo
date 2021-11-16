"""
This example demonstrates the situate argument to print.
"""

from quo import Console
from quo.panel import Panel
console = Console(width=20, height=49)

style = "blue"
panel = Panel("Quo", style="on red", expand=False)
console.echo(panel, fg=style)
console.echo(panel, fg=style, situate="left")
console.echo(panel, fg=style, situate="center")
console.echo(panel, fg=style, situate="right")
