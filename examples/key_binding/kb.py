import os

from quo.keys import bind
from quo.prompt import Prompt

session = Prompt()

# Print "Hello world" when ctrl-h is pressed

@bind.add("ctrl-h")

def _(event):
    print("Hello, World!")
    os.system("ls")

#session.prompt(">> ")



if __name__ == "__main__":
    _(event)
