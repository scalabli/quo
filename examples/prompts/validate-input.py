from quo import echo
from quo.prompt import Prompt

session = Prompt(int=True)
number = int(session.prompt('Give a number: '))
echo('You said: %i' % number)
