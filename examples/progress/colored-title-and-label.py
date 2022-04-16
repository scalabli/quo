#!/usr/bin/env python
"""
A progress bar that displays a formatted title above the progress bar and has a
colored label.
"""
import time

from quo.text import Text
from quo.progress import ProgressBar

def main():
    title = Text('Downloading <style bg="yellow" fg="black">4 files...</style>')
    label = Text("<red>some file</red>: ")

    with ProgressBar(title=title) as pb:
        for i in pb(range(800), label=label):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
