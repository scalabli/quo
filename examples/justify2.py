"""
This example demonstrates the justify argument to print.
"""

from quo.console import Console
from quo.panel import Panel

console = Console(width=20)

style = "blue"
panel = Panel("Quo", style="on red", expand=False)
console.evoke(panel, style=style)
console.evoke(panel, style=style, justify="left")
console.evoke(panel, style=style, justify="center")
console.evoke(panel, style=style, justify="right")
