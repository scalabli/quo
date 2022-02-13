#!/usr/bin/env python
"""
Demonstration of all the ANSI colors.
"""
import quo
from quo.text import Text

def main():
    tokens = quo.text.FormattedText([("fg:" + name, name + "  ") for name in quo.color.NAMED_COLORS])

    quo.inscribe(Text("\n<u>Named colors, using 16 color output.</u>"))
    quo.inscribe("Note that it doesn't really make sense to use named colors ")
    quo.inscribe("with only 16 color output.)")
    quo.inscribe(tokens, color_depth=quo.color.ColorDepth.four_bit)

    quo.inscribe(Text("\n<u>Named colors, use 256 colors.</u>"))
    quo.inscribe(tokens)

    quo.inscribe(Text("\n<u>Named colors, using True color output.</u>"))
    quo.inscribe(tokens, color_depth=quo.color.ColorDepth.twenty_four_bit)


if __name__ == "__main__":
    main()
