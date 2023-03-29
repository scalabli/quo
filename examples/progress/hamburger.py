import time

from quo.progress import ProgressBar

with ProgressBar(spinner="hamburger") as pb:
    for i in pb(range(800)):
        time.sleep(0.01)