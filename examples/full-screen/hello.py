from quo import container
from quo.widget import Label


content = Label("Hello, World")

container(content, bind=True, full_screen=True)
