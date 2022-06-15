from quo import echo

from quo.console import Console

c = Console()

c.bar("dddd")

echo(locals(), fg="blue", bg='green')
