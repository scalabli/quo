import datetime

from quo import container
from quo.widget import Box
from quo.keys import bind
from quo.layout import FormattedTextControl as FTC
from quo.text import Text
from quo.window import Window

def get_time():
    now = datetime.datetime.now()
    return [
            ("bg:green fg:black", "%s:%s:%s"  % (now.hour, now.minute, now.second))
            ]

content = Box(Window(FTC(get_time), align="center"))


@bind.add("ctrl-c")
def _(event):
    event.app.exit()

container(content,bind=True, full_screen=True)
