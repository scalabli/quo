from time import sleep
from quo import echo, Console


console = Console()

tasks = [f"task {n}" for n in range(1, 11)]
echo(f"Working on tasks...", fg="green", bold=True)
with console.status("[bold green] ",) as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
