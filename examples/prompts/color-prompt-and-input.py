from quo.prompt import Prompt

session = Prompt(fg="red", bg="blue")

session.prompt(">> ")



from quo.color import Color
from quo.prompt import Prompt

style = Color("fg:blue") # User input (default text)

session = Prompt(fg="blue")


session.prompt("<red>john</red><white>@</white><green>localhost</green><red>:</red><cyan><u>/user/john</u></cyan><purple>$ </purple>")


