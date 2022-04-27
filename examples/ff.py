from quo import container
from quo.buffer import Buffer
from quo.layout import BufferControl, FormattedTextControl, VSplit, Window

buffer1 = Buffer()  # Editable buffer.

content = VSplit([
       # One window that holds the BufferControl with the default buffer on the left.
     Window(BufferControl(buffer=buffer1)),

       # A vertical line in the middle. We explicitly specify the width, to
       # make sure that the layout engine will not try to divide the whole
       # width by three for all these windows. The window will simply fill its
       # content by repeating this character.
     Window(width=1, height=1, char='|'),

       # Display the text 'Hello world' on the right.
     Window(FormattedTextControl('Hello world')),
 ])


container(content, bind=True, full_screen=True)
   # You won't be able to Exit this a
