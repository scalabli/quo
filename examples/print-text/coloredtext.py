"""
Demonstration of all the ANSI colors.
"""

from quo import print

print("<u>Foreground colors</u>")

print('<red>This is red</red>')
print('<green>This is green</green>')
print('<cyan>This is cyan</cyan>')



print("\nNamed colors (256 color palette, or true color)")
     
print('<skyblue>This is sky blue</skyblue>')   
print('<seagreen>This is sea green</seagreen>')
print('<violet>This is violet</violet>')

print('<style fg="white" bg="green">White on green</style>')


from quo.style import Style

style = Style.add({
      'aaa': 'fg:red',
     'bbb': 'fg:blue italic'
     })

print('<aaa>Hello</aaa> <bbb>world</bbb>!', style=style)

    