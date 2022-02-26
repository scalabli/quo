#!/usr/bin/env python
"""
Demonstration of how to print using the Text class.
"""
from quo import print
from quo.text import Text

text = "Demonstration of how to print using the text class"


print(Text("\n<u><b>{}</b></u>").format(text))

print(Text("    <b>Bold</b>"))
print(Text("    <blink>Blink</blink>"))
print(Text("    <i>Italic</i>"))
print(Text("    <reverse>Reverse</reverse>"))
print(Text("    <u>Underline</u>"))
print(Text("    <s>Strike</s>"))
print(Text("    <hidden>Hidden</hidden> (hidden)"))

    # Ansi colors

print("ANSI COLORS")
print(Text("    <ansired>ANSI Red</ansired>"))
print(Text("    <ansiblue>ANSI Blue</ansiblue>"))

    # Other named colors.
print("NAMED COLORS")
print(Text("    <orange>orange</orange>"))
print(Text("    <purple>purple</purple>"))
print(Text("    <khaki>khaki</khaki>"))

    # Background colors.
 #   title("Background colors")

 #   quo.inscribe(quo.text.HTML('    <style fg="ansiwhite" bg="ansired">ANSI Red</style>'))
 #   quo.inscribe(quo.text.HTML('    <style fg="ansiwhite" bg="ansiblue">ANSI Blue</style>'))

 #   # Interpolation.




 #   title("HTML interpolation (see source)")

print(Text('<i>{}</i>').format("<test>"))
print(Text('  <b>{text}</b>').format(text="<test>"))
print(Text('    <u>%s</u>') % ("<text>"))
