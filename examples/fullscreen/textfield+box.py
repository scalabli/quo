from quo import container
from quo.box import Box
from quo.label import Label
 
# Layout for displaying hello world.
# (The box takes care of the margin/padding.)

label = Label("Hello, world!!", fg="purple", italic=True, underline=True)
 
content = Box(label, char="!")

container(content, bind=True, full_screen=True)