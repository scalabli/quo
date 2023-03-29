#!/usr/bin/env python
"""
A simple progress bar, visualised with rainbow colors (for fun).
"""
import time

from quo.progress import ProgressBar


with ProgressBar("Rainbow Progressbar", rainbow=True, spinner="arrows") as pb:
        for i in pb(range(20), label="Downloading...", auto_hide=True):
            time.sleep(0.1)

