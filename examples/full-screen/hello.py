from quo import container
from quo.console import get_app
from quo.widget import Label


content = Label("Hello, World")

get_app().layout.focus(content)
container(content)
