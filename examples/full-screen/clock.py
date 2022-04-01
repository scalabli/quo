import datetime

from quo import container
from quo.keys import bind
from quo.text import Text
from quo.layout import Window, FormattedTextControl as FC
from quo.widget import Label

def get_time():
    now = datetime.datetime.now()
    return [
            ("bg:green fg:black", "%s:%s:%s"  % (now.hour, now.minute, now.second))
            ]

content = Window(FC(get_time), align="center")


@bind.add("ctrl-c")
def _(event):
    event.app.exit()

#Console(layout=lay, bind=bind, refresh_interval=0.8).run()
container(content,  bind=True, full_screen=True)
