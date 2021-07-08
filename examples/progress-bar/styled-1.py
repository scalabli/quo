#!/usr/bin/env python
"""
A very simple progress bar which keep track of the progress as we consume an
iterator.
"""
import quo
import time
from quo.output import flair
from quo import ProgressBar
   #     "title": "#4444ff underline",
#        "label": "#ff4400 bold",
#        "percentage": "#00ff00",
  #      "bar-a": "bg:#00ff00 #004400",
  #      "bar-b": "bg:#00ff00 #000000",
   #     "bar-c": "#000000 underline",
  #      "current": "#448844",
  #      "total": "#448844",
#        "time-elapsed": "#444488",
   #     "time-left": "bg:#88ff88 #000000",
 #   }
#)

title = "Progress bar example with custom styling"
label = "Downloading..."


def main():
    with ProgressBar(
            quo.flair(f"{title}")
       # style=style, title="Progress bar example with custom styling."
    ) as pb:
        for i in pb(range(1600)
             #   flair(f"{label}", fg="black")
                time.sleep(0.01)


if __name__ == "__main__":
    main()
