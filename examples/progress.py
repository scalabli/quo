import time

from quo import Suite
from quo.progress.progress import Progress
from quo.keys import KeyBinder
from quo.layout.layout import Layout

kb = KeyBinder()

@kb.add("q")
def _(quit):
    quit.app.exit()

appli = Suite(key_bindings=kb, full_screen=False)
appli.run


with Progress() as progress:

    task1 = progress.add_task("[red]Downloading...", total=1000)
    task2 = progress.add_task("[green]Processing...", total=1000)
    task3 = progress.add_task("[cyan]Cooking...", total=1000)

    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=0.3)
        progress.update(task3, advance=0.9)
        time.sleep(0.02)




@kb.add("q")
def _(quit):
    quit.app.exit()



suite = Suite(key_bindings=kb, full_screan=True)

suite.run()

