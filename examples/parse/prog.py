from quo.parse import Parser

parser = Parser(description="This script prints hello NAME COUNT times.")

parser.argument("--count", default=3, type=int, help="number of greetings")
parser.argument('name', help="The person to greet")

arg = parser.parse()

for x in range(arg.count):
        print(f"Hello {arg.name}!")

    

