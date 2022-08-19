from quo.highlight import Python
from quo.widget import TextField
from quo import container

def Syntax(code=None, theme=Python, path=False):

    if path is True:
        with open(code, "rb") as f:
            code = f.read().decode("utf-8")
            
    tf = TextField(
            text=code,
            read_only=True,
            scrollbar=True,
            line_numbers=True,
            multiline=True,
            highlighter=theme
            )
    container(tf)

#class Syntax:

#    def __init__(self, code:str=None, theme=None):

     #   if theme is None:
         #   theme = Python

      #  TextField(
            #    text=code,
              #  read_only=True,
              #  scrollbar=True,
               # line_numbers=True,
           #     multiline=True,
               # search_field=search_field,
               # highlighter=theme
              #  )
