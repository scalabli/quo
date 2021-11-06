from time import sleep
from quo import Console
from quo.keys import KeyBinder

console = Console()
kb = KeyBinder()
console.echo()

@kb.add("ctrl-c")
def _(quit):
    quit.app.exit()

tasks = [f"task {n}" for n in range(1, 11)]

with console.status("[bold green]Working on tasks... Press ctrl-c to quit",) as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
