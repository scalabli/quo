from quo import container, echo
from quo.widget import Label

from quo.table import Table


data = [
        ["Name", "Gender", "Age"],
        ["Alice", "F", 24],
        ["Bob", "M", 19],
        ["Dave", "M", 24]
        ]

content = Label(Table(data), style="fg:00FFFFFF bg:purple")

from quo.keys import bind

@bind.add("ctrl-d")
def _(event):
    event.app.exit()

container(content, bind=True, full_screen=True)
