#!/usr/bin/env python
"""
Example of nested progress bars.
"""
import time

from quo.progress import ProgressBar


title='<blue>Nested progress bars</blue>'
toolbar="<b>[Control-L]</b> clear  <b>[Control-C]</b> abort"


with ProgressBar(title, bottom_toolbar=toolbar)as pb:
    for i in pb(range(6), label="Main task"):
        for j in pb(range(200), label=f"Subtask  <%d>" % (i + 1,), auto_hide=True):
            time.sleep(0.01)

