#!/usr/bin/env python
"""
Demonstration of all the ANSI colors.
"""
from quo import print
from quo.color import ColorDepth, NAMED_COLORS
from quo.text import Text, FormattedText

def main():
    tokens = FormattedText([("fg:" + name, name + "  ") for name in NAMED_COLORS])

    print(Text("\n<u>Named colors, using 16 color output.</u>"))
    print("Note that it doesn't really make sense to use named colors ")
    print("with only 16 color output.)")
    print(tokens, color_depth=ColorDepth.four_bit)

    print(Text("\n<u>Named colors, use 256 colors.</u>"))
    print(tokens)

    print(Text("\n<u>Named colors, using True color output.</u>"))
    print(tokens, color_depth=ColorDepth.twenty_four_bit)


if __name__ == "__main__":
    main()
