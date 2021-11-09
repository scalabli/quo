from time import sleep
from quo import Console


console = Console()

tasks = [f"task {n}" for n in range(1, 11)]

with console.status("[bold green]Working on tasks...",) as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
