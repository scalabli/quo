from quo.prompt import Prompt
from quo.completion import WordCompleter

example = WordCompleter(['USA', 'UK', 'Canada', 'Kenya'])

session = Prompt(completer=example)
session.prompt('Which country are you from?: ')
