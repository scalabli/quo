from quo import evoke
from quo.console import group
from quo.panel import Panel


@group()
def get_panels():
    yield Panel("Hello", style="on blue")
    yield Panel("World", style="on red")


evoke(Panel(get_panels()))
