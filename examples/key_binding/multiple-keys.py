from quo.keys import bind
from quo.prompt import Prompt

session = Prompt()

@bind.add("q", "u", "o")
def _(event):
    import os
    os.system("webprobe")
    print("QUO")


session.prompt(">> ")
