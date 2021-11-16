from quo import Console
from quo.pretty import Pretty
from quo.panel import Panel


DATA = "My name is Quo"



console = Console()
for w in range(130):
    console.echo(Panel(Pretty(DATA), width=w))
