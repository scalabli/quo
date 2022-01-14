#!/usr/bin/env python
"""
A simple progress bar, visualised with rainbow colors (for fun).
"""
import time
import quo


from quo.progress import formatters



def main():
    true_color = quo.confirm("Yes true colors? (y/n) ")

    custom_formatters = [
        formatters.Label(),
        formatters.Text(" "),
        formatters.Rainbow(formatters.Bar()),
        formatters.Text(" left: "),
        formatters.Rainbow(formatters.TimeLeft()),
    ]

    if true_color:
        color_depth = quo.color.ColorDepth.four_bit
    else:
        color_depth = quo.color.ColorDepth.eight_bit

    with quo.ProgressBar(formatters=custom_formatters, color_depth=color_depth) as pb:
        for i in pb(range(20), label="Downloading..."):
            time.sleep(1)


if __name__ == "__main__":
    main()
