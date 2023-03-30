
from quo import container
from quo.widget import Frame, Label

content = Frame(
        Label("Hello, World!"),
        title="Quo: python")

#Press Ctrl-C to exit
container(content, bind=True, full_screen=True)
