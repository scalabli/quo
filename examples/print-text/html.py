#!/usr/bin/env python
"""
Demonstration of how to print using the HTML class.
"""
import quo

@quo.tether()
def main():
    pass

@quo.command()
@quo.app("--text", help="Demonstration of how to print using HTML")
def title(text):
    quo.inscribe(quo.text.HTML("\n<u><b>{}</b></u>").format(text))

@quo.command()
@quo.app("--formatting", help="Demonstration of special formatting")
def format(formatting):
    title("Special formatting")
    quo.inscribe(quo.text.HTML("    <b>Bold</b>"))
    quo.inscribe(quo.text.HTML("    <blink>Blink</blink>"))
    quo.inscribe(quo.text.HTML("    <i>Italic</i>"))
    quo.inscribe(quo.text.HTML("    <reverse>Reverse</reverse>"))
    quo.inscribe(quo.text.HTML("    <u>Underline</u>"))
    quo.inscribe(quo.text.HTML("    <s>Strike</s>"))
    quo.inscribe(quo.text.HTML("    <hidden>Hidden</hidden> (hidden)"))

    # Ansi colors.
    title("ANSI colors")

    quo.inscribe(quo.text.HTML("    <ansired>ANSI Red</ansired>"))
    quo.inscribe(quo.text.HTML("    <ansiblue>ANSI Blue</ansiblue>"))

    # Other named colors.
    title("Named colors")

    quo.inscribe(quo.text.HTML("    <orange>orange</orange>"))
    quo.inscribe(quo.text.HTML("    <purple>purple</purple>"))

    # Background colors.
    title("Background colors")

    quo.inscribe(quo.text.HTML('    <style fg="ansiwhite" bg="ansired">ANSI Red</style>'))
    quo.inscribe(quo.text.HTML('    <style fg="ansiwhite" bg="ansiblue">ANSI Blue</style>'))

 #   # Interpolation.
 #   title("HTML interpolation (see source)")

 #   quo.inscribe((quo.text.HTML('<i>{}</i>').format("<test>"))
#    quo.inscribe(quo.text.HTML('  <b>{text}</b>').format(text="<test>"))
 #   quo.inscribe(quo.text.HTML('    <u>%s</u>') % ("<text>",))

 #   print()


main.addcommand(title)
main.addcommand(format)


if __name__ == "__main__":

    main()
