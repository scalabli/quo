from quo.color import Color
from quo.prompt import Prompt

style = Color("fg:red")

session = Prompt(style=style)

session.prompt("Type something: ")
