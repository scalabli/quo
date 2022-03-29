from quo.console import Console
from quo.layout import Layout
from quo.widget import Label


content = Label("ddd")

lay = Layout(content)

Console(layout=lay).run()
