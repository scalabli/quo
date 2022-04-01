#!/usr/bin/env python
"""
Example of nested progress bars.
"""
import time

from quo.progress import ProgressBar
from quo.text import Text


def main():
    with ProgressBar(
        title=Text('<blue>Nested progress bars</blue>'),
        bottom_toolbar=Text("<b>[Control-L]</b> clear  <b>[Control-C]</b> abort")
        )as pb:

        for i in pb(range(6), label="Main task"):
            for j in pb(
                range(200), label="Subtask <%s>" % (i + 1,), remove_when_done=True
            ):
                time.sleep(0.01)


if __name__ == "__main__":
    main()
