import time

from quo.progress import ProgressBar

toolbar = "Press <b>CTRL+C</b> to quit"

with ProgressBar(bottom_toolbar=toolbar) as pb:
    for i in pb(range(800)):
        time.sleep(.01)
