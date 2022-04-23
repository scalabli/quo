from quo.keys import bind
from quo.prompt import Prompt

session = Prompt()

@bind.add("q", "u", "o")
def _(event):
    print("QUO")


session.prompt(">> ")
