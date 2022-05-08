from quo.color import Color
from quo.prompt import Prompt

style = Color("fg:blue bg:green")

session = Prompt(style=style)

message = [
        ('fg:red', 'john'),
        ('fg:white', '@'),
        ('fg:green bg:white', 'localhost'),
        ('fg:yellow', ':'),
        ('fg:cyan underline', '/user/john'),
        ('fg:red', '$ ')
        ]

session.prompt(message)
