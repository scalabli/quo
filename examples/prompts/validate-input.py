from quo import echo
from quo.prompt import Prompt
from quo.types import integer

session = Prompt()

type = integer()
number = int(session.prompt('Give a number: ', type=type))
echo('You said: %i' % number)
