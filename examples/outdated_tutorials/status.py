from time import sleep
import quo


console = quo.Console()

tasks = [f"task {n}" for n in range(1, 11)]
quo.echo(f"Working on tasks...", fg="green", bold=True)
with console.status("[bold green] ",) as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
