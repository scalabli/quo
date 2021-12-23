#!/usr/bin/env python
"""
Demonstration of how to print using the HTML class.
"""
import quo

from quo.shortcuts.utils import print_formatted_text

print = print_formatted_text

@quo.command()
@quo.app("--text", help="Demonstration of how to print using HTML")
def title(text):
    print(quo.text.HTML("\n<u><b>{}</b></u>").format(text))

@quo.app("--formatting", help="Demonstration of special formatting")

def main(formatting):
    title("Special formatting")
    print(quo.text.HTML("    <b>Bold</b>"))
    print(quo.text.HTML("    <blink>Blink</blink>"))
    print(quo.text.HTML("    <i>Italic</i>"))
    print(quo.text.HTML("    <reverse>Reverse</reverse>"))
    print(quo.text.HTML("    <u>Underline</u>"))
    print(quo.text.HTML("    <s>Strike</s>"))
    print(quo.text.HTML("    <hidden>Hidden</hidden> (hidden)"))

    # Ansi colors.
    title("ANSI colors")

    print(quo.text.HTML("    <ansired>ANSI Red</ansired>"))
    print(quo.text.HTML("    <ansiblue>ANSI Blue</ansiblue>"))

    # Other named colors.
    title("Named colors")

    print(quo.text.HTML("    <orange>orange</orange>"))
    print(quo.text.HTML("    <purple>purple</purple>"))

    # Background colors.
    title("Background colors")

    print(quo.text.HTML('    <style fg="ansiwhite" bg="ansired">ANSI Red</style>'))
    print(quo.text.HTML('    <style fg="ansiwhite" bg="ansiblue">ANSI Blue</style>'))

    # Interpolation.
    title("HTML interpolation (see source)")

    print(quo.text.HTML("    <i>{}</i>").format("<test>"))
    print(quo.text.HTML("    <b>{text}</b>").format(text="<test>"))
    print(quo.text.HTML("    <u>%s</u>") % ("<text>",))

    print()


if __name__ == "__main__":
    main()
