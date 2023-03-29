import time

from quo.progress import ProgressBar

with ProgressBar(spinner="dots3") as pb:
    for i in pb(range(800)):
        time.sleep(0.01)