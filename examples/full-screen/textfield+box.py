from quo import container
from quo.box import Box
from quo.label import Label
from quo.window import Window
 
# Layout for displaying hello world.
# (The box takes care of the margin/padding.)

label = Labe("Hello, world!!")
window = Window(label)
 
content = Box(window, char="!")

container(content, bind=True, full_screen=True)