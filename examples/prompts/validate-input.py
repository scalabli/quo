from quo import echo
from quo.prompt import Prompt
from quo.types import Number

session = Prompt()

number = int(session.prompt('Give a number: ', type=Number()))

echo('You said: %i' % number)
