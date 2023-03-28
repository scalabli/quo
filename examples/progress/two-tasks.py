#!/usr/bin/env python
"""
Two progress bars that run in parallel.
"""
import threading
import time
from quo.progress import ProgressBar

with ProgressBar("<red>TWO TASKS</red>", start="dd", spinner="hamburger") as pb:
    # Two parallal tasks.
    def task1():
        for i in pb(range(100)):
            time.sleep(0.05)

    def task2():
        for i in pb(range(150)):
            time.sleep(0.08)

    # Start threads.
    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()

    # Wait for the threads to finish. We use a timeout for the join() call,
    # because on Windows, join cannot be interrupted by Control-C or any other # signal.
    for t in [t1, t2]:
        while t.is_alive():
            t.join(timeout=.5)

