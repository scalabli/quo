#!/usr/bin/env python
"""
A progress bar that displays a formatted title above the progress bar and has a
colored label.
"""
import time

from quo.progress import ProgressBar

title = "Downloading <style bg='yellow' fg='black'>4 files...</style>"

label = "<red>some file</red>: "

with ProgressBar(title) as pb:
    for i in pb(range(800), label):
        time.sleep(0.01)

