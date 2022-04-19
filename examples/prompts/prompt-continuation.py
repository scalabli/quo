from quo.prompt import Prompt

session = Prompt(multiline=True, continuation=True)
session.prompt('multiline input> ')

