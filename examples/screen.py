"""
Demonstration of Console.screen() 
"""
from time import sleep
from quo.keys import KeyBinder
from quo.align import Align
from quo.console import Console
from quo.panel import Panel

console = Console()
kb = KeyBinder()
@kb.add("ctrl-c")
def q(quit):
    quit.app.exit()
with console.screen(style="bold white on red") as screen:
    text = Align.center("[blink]Press Ctrl-C to quit[/blink]", vertical="middle")
    screen.update(Panel(text))
    sleep(10)
