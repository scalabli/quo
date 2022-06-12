from quo.console import Console

console = Console()

@console.command()
@console.app('--count', default=1, help='number of greetings')
@console.app('--name', prompt="What is your name?", help="The person to greet")

def hello(count: int, name: str):
    """This script prints hello NAME COUNT times."""
    for x in range(count):
        print(f"Hello {name}!")

if __name__ == "__main__":
    hello()
