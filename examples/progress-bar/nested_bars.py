#!/usr/bin/env python
"""
Example of nested progress bars.
"""
import quo
import time
from quo import HTML, ProgressBar, flair


def main():
    with ProgressBar(
        title = flair(f"Nested progress bars", fg="blue", bold=True),
      #  title=HTML('<b fg="#aa00ff">Nested progress bars</b>'),
        bottom_toolbar=HTML(" <b>[Control-L]</b> clear  <b>[Control-C]</b> abort"),
    ) as pb:

        for i in pb(range(6), label="Main task"):
            for j in pb(
                range(200), label="Subtask <%s>" % (i + 1,), remove_when_done=True
            ):
                time.sleep(0.01)


if __name__ == "__main__":
    main()
