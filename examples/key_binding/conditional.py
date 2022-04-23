import datetime

from quo.filters import Condition
from quo.keys import bind
from quo.prompt import Prompt

session = Prompt()

@Condition
def is_active():
    " Only activate key binding on the second half of each minute. "

    return datetime.datetime.now().second > 30


@bind.add('ctrl-t', filter=is_active)
def _(event):
    import os
    os.system("ls")
    print("Hello world")
        # ...

session.prompt("")
