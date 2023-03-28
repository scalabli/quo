#!/usr/bin/env python
"""
A very simple progress bar which keep track of the progress as we consume an
iterator.
"""
import time

from quo.progress import ProgressBar

with ProgressBar() as pb:
    for i in pb(range(800)):
        time.sleep(0.01)