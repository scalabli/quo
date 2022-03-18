#!/usr/bin/env python
"""
A very simple progress bar which keep track of the progress as we consume an
iterator.
"""
import os
import signal
import time

from quo.text import Text
from quo.keys import bind
#from quo.patch_stdout import patch_stdout
from quo.progress import ProgressBar


def main():
    bottom_toolbar = Text(
        ' <b>[f]</b> Print "f" <b>[q]</b> Abort  <b>[x]</b> Send Control-C.'
    )

    # Create custom key bindings first
    cancel = [False]

    @bind.add("f")
    def _(event):
        print("You pressed `f`.")

    @bind.add("q")
    def _(event):
        "Quit by setting cancel flag."
        cancel[0] = True

    @bind.add("x")
    def _(event):
        "Quit by sending SIGINT to the main thread."
        os.kill(os.getpid(), signal.SIGINT)

    # Use `patch_stdout`, to make sure that prints go above the
    # application.
  #  with patch_stdout():
    with ProgressBar(bottom_toolbar=bottom_toolbar) as pb:
            for i in pb(range(800)):
                time.sleep(0.01)

                if cancel[0]:
                    break


if __name__ == "__main__":
    main()
