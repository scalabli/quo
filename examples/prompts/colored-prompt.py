from quo.prompt import Prompt
from quo.style import Style


style = Style.add({' ':'fg:red bg:green'}) #User input (default text)

session = Prompt(style=style)

session.prompt("Type something: ")
