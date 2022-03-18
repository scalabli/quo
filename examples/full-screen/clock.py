import datetime

from quo.console import Console
from quo import container
from quo.keys import Bind
from quo.text import Text
from quo.layout import Layout
from quo.widget import Label
from quo.layout import Window, FormattedTextControl as FC

now = datetime.datetime.now()

bind = Bind()

c_time = "%s:%s:%s" %  (now.hour, now.minute, now.second)

def get_prompt():
    "Tokens to be shown before the prompt."
    now = datetime.datetime.now()
    return [
            ("bg:green fg:black", "%s:%s:%s"  % (now.hour, now.minute, now.second)),
            ("bg:cornsilk fg:maroon", "Enter something: ")
            ]
content = Window(FC(get_prompt))

lay = Layout(content)

@bind.add("ctrl-c")
def _(event):
    event.app.exit()

Console(layout=lay, bind=bind, refresh_interval=0.8).run()
#ontainer(content, bind=True, full_screen=True)
