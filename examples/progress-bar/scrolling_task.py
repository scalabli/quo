#!/usr/bin/env python
"""
A very simple progress bar where the name of the task scrolls, because it's too long.
iterator.
"""
import quo
import time
from quo import ProgressBar, flair


def main():
    with ProgressBar(
        title = flair(f"Scrolling task name", fg="vyellow")
    ) as pb:
        for i in pb(
            range(800),
            label="This is a very very very long task that requires horizontal scrolling ...",
        ):
            time.sleep(0.01)


if __name__ == "__main__":
    main()