from quo import container
from quo.buffer import Buffer
from quo.document import Document
from quo.keys import bind
from quo.layout import HSplit, VSplit, Window

from quo.layout.controls import BufferControl, FormattedTextControl

# 1. The layout
top_text = (
    "Focus example.\n"
    "[q] Quit [a] Focus left top [b] Right top [c] Left bottom [d] Right bottom."
)

content = """
Quo is a Python based toolkit for writing Command-
Line Interface(CLI) applications. Quo is making 
headway towards composing speedy and orderly CLI 
applications while forestalling any disappointments 
brought about by the failure to execute a CLI API. 
Simple to code, easy to learn, and does not come with needless baggage. """


left_top = Window(
        BufferControl(
            Buffer(document=Document(content)
                )
            )
        )
left_bottom = Window(BufferControl(Buffer(document=Document(content))))
right_top = Window(BufferControl(Buffer(document=Document(content))))
right_bottom = Window(BufferControl(Buffer(document=Document(content))))


content = HSplit([

     Window(FormattedTextControl(top_text), height=2, style="reverse"),
     Window(height=1, char="-"),  # Horizontal line in the middle.
     VSplit([
         left_top,
         Window(width=1, char="|"),
         right_top
         ]),
     Window(height=1, char="-"),  # Horizontal line in the middle.
     VSplit([
         left_bottom,
         Window(width=1, char="|"),
         right_bottom
         ])
     ])


# 2. key bindings
@bind.add("a")
def _(event):
    event.app.layout.focus(left_top)


@bind.add("b")
def _(event):
    event.app.layout.focus(right_top)


@bind.add("c")
def _(event):
    event.app.layout.focus(left_bottom)


@bind.add("d")
def _(event):
    event.app.layout.focus(right_bottom)


@bind.add("tab")
def _(event):
    event.app.layout.next()


@bind.add("s-tab")
def _(event):
    event.app.layout.previous()


# 3. The `Application`

container(content, bind=True, full_screen=True)
