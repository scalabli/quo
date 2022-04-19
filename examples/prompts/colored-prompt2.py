from quo.prompt import Prompt
from quo.style import Style

style = Style.add({' ':'fg:blue'}) # User input (default text)
session = Prompt(style=style)

message = [
        ('fg:red', 'john'),
        ('fg:white', '@'),
        ('fg:green bg:white', 'localhost'),
        ('fg:yellow', ':'),
        ('fg:cyan underline', '/user/john'),
        ('fg:red', '$ ')
        ]

session.prompt(message, ('fg:red', 'dfff'))
