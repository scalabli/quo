#!/usr/bin/env python
"""
A very simple progress bar which keep track of the progress as we consume an
iterator.
"""
import time
from quo.progress import ProgressBar
from quo.style import Style


style = Style.add(
    {
        "title": "#4444ff underline",
        "label": "#ff4400 bold",
        "percentage": "red", ##00ff00",
        "bar-a": "bg:#00ff00 #004400",
        "bar-b": "bg:#00ff00 #000000",
        "bar-c": "#000000",
        "current": "#448844",
        "total": "#448844",
        "time-elapsed": "#444488",
        "time-left": "bg:#88ff88 #000000",
    }
)


with ProgressBar("<b><maroon>Progress bar example with custom styling.</maroon></b>") as pb:
    for i in pb(range(1600), label="<blue>Downloading...</blue>"):
        time.sleep(0.01)
