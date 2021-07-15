#!/usr/bin/env python
"""
A simple progress bar, visualised with rainbow colors.
"""
import quo
import time
from quo import ColorDepth, ProgressBar, pause
from quo.indicators import formatters



def main():
    forward = pause()
    custom_formatters = [
        formatters.Label(),
        formatters.Text(" "),
        formatters.Rainbow(formatters.Bar()),
        formatters.Text(" left: "),
        formatters.Rainbow(formatters.TimeLeft()),
    ]

    if forward:
        color_depth = ColorDepth.DEPTH_24_BIT
    else:
        color_depth = ColorDepth.DEPTH_8_BIT

    with ProgressBar(formatters=custom_formatters, color_depth=color_depth) as pb:
        for i in pb(range(20), label="Downloading..."):
            time.sleep(1)


if __name__ == "__main__":
    main()
