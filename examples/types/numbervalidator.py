from quo import echo
from quo.prompt import Prompt
from quo.types import integer

session = Prompt()

number = int(session.prompt('Give a number: ', type=integer()))

echo(f"You said: {number}")
