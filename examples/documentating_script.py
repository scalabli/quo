from quo import print
from quo.console import command
from quo.console import app

@command()
@app('--count', default=1, help='number of greetings')
@app('--name', prompt="What is your name?", help="The person to greet")

def hello(count: int, name: str):
    """This script prints hello NAME COUNT times."""
    for x in range(count):
        print(f"Hello {name}!")

if __name__ == "__main__":
    hello()
