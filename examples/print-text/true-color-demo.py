#!/usr/bin/env python
"""
Demonstration of all the ANSI colors.
"""
import quo

@quo.command()
@quo.app("@colors", help="Demonstration of ANSI colors")
def _color(colors):
    quo.inscribe(quo.text.HTML("\n<u>True color test.</u>"))

    for template in [
        "bg:#{0:02x}0000",  # Red.
        "bg:#00{0:02x}00",  # Green.
        "bg:#0000{0:02x}",  # Blue.
        "bg:#{0:02x}{0:02x}00",  # Yellow.
        "bg:#{0:02x}00{0:02x}",  # Magenta.
        "bg:#00{0:02x}{0:02x}",  # Cyan.
        "bg:#{0:02x}{0:02x}{0:02x}",  # Gray.
    ]:
        fragments = []
        for i in range(0, 256, 4):
            fragments.append((template.format(i), " "))

        quo.inscribe(quo.text.FormattedText(fragments), color_depth=quo.color.ColorDepth.DEPTH_4_BIT)
        quo.inscribe(quo.text.FormattedText(fragments), color_depth=quo.color.ColorDepth.DEPTH_8_BIT)
        quo.inscribe(quo.text.FormattedText(fragments), color_depth=quo.color.ColorDepth.DEPTH_24_BIT)
        quo.inscribe()


if __name__ == "__main__":
    _color()
