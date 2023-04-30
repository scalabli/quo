
from quo import container
from quo.frame import Frame
from quo.label import Label

content = Frame(
        Label("Hello, World!"),
        title="<red>Quo: python</red>",
        frame_color="green")

#Press Ctrl-C to exit
container(content, bind=True, full_screen=True)
