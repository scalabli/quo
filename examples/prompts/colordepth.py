from quo.prompt import Prompt
from quo.color import ColorDepth


session = Prompt(color_depth=ColorDepth.eight_bit)

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
