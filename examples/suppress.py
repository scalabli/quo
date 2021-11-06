import quo
from quo.traceback import install

install(suppress=[quo])

from quo import command, app, echo, prompt
@command()
@app("--count", default=1, help="Number of greetings.")

name = prompt(" ")
def hello(count):
    """Simple program that greets NAME for a total of COUNT times."""
 #   1 / 0
    for x in range(count):
        name = prompt("What is your name?")
        echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()
