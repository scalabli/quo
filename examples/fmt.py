#from quo import print
from quo.shortcuts.utils import _print
from quo.text import FormattedText as v
text =v([
    [
     ('fg:red', 'Hello'),
     ('', ' '),
     ('fg:purple italic', 'World')
     ]
    ]
     )
print(text) #fmt=True)
