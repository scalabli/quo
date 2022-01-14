"""
Demonstration of Console.screen() 
"""
from time import sleep
from quo import Console
from quo.align import Align
from quo.panel import Panel

console = Console()

with console.screen(style="bold white on red") as screen:
    text = Align.center("[blink] [/blink]", vertical="middle")
    screen.update(Panel(text))
    sleep(10)
