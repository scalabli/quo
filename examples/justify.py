"""
This example demonstrates the justify argument to print.
"""

from quo.console import Console

console = Console(width=20)

style = "bold white on blue"
console.evoke("Quo", style=style)
console.evoke("Quo", style=style, justify="left")
console.evoke("Quo", style=style, justify="center")
console.evoke("Quo", style=style, justify="right")
