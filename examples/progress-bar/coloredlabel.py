#!/usr/bin/env python
"""
A progress bar that displays a formatted title above the progress bar and has a
colored label.
"""
import time
from quo import ProgressBar, flair


def main():
    title = flair(f"Downloading", fg="black", bg="vyellow")
    label =flair(f"Some file", fg="red")

    with ProgressBar(title=title) as pb:
        for i in pb(range(800), label=label):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
