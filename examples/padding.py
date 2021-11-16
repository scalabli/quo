from quo import echo, Console, Padding


console = Console()
test = Padding("Hello", (2, 4), style="on blue", expand=False)
console.echo(test, fg="red")

