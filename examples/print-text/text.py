#!/usr/bin/env python
"""
Demonstration of how to print using the Text class.
"""
from quo import echo, print

text = "Demonstration of how to print using the text class"


#echo("\n<u><b>{}</b></u>").format(text)

print("    <b>Bold</b>")
print("    <blink>Blink</blink>")
print("    <i>Italic</i>")
print("    <reverse>Reverse</reverse>")
print("    <u>Underline</u>")
print("    <s>Strike</s>")
print("    <hidden>Hidden</hidden> (hidden)")

    # Ansi colors

print("ANSI COLORS")
print("    <ansired>ANSI Red</ansired>")
print("    <ansiblue>ANSI Blue</ansiblue>")

    # Other named colors.
print("NAMED COLORS")
print("    <orange>orange</orange>")
print("    <purple>purple</purple>")
print("    <khaki>khaki</khaki>")

#print('<i>{}</i>').format("<test>")
#print('  <b>{text}</b>').format(text="<test>")
#print('    <u>%s</u>') % ("<text>")
