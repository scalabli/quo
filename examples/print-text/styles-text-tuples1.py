from quo import print
from quo.text import FormattedText

text = FormattedText([
    ('fg:red', 'Hello'),
    ('', ' '),
    ('fg:purple italic', 'World')
    ])

print(text, fmt=True)
