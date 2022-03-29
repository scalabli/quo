from quo import print
from quo.style import Style
from quo.text import FormattedText

# The text.
text = FormattedText([
    ('class:aaa', 'Hello'),
    ('', ' '),
    ('class:bbb', 'World'),
    ])                                                     

# The style sheet.
style = Style.add({
    'aaa': 'fg:green',
    'bbb': 'fg:blue italic',
    })


print(text, fmt=True, style=style)
