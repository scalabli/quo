from quo.prompt import Prompt
from quo.style import Style


style = Style.add({' ':'fg:blue'}) # User input (default text)
session = Prompt(color_depth="true_color", style=style)

message = [
       ('fg:red', 'john'),
       ('fg:white', '@'),
       ('fg:green bg:white', 'localhost'),
       ('fg:yellow', ':'),
       ('fg:cyan underline', '/user/john'),
       ('fg:red', '$ ')
   ]


session.prompt(message)

#m quo.color import ColorDepth

 #   session = Prompt(
   #             style=style,
     #           color_depth=ColorDepth.TRUE_COLOR
    #            )


 #   session.prompt(message)
