#!/usr/bin/env python
"""
Example of an input box dialog.
"""
import time
import multiprocessing
from quo import print
from quo.dialog import InputBox

#start_time = time.time()

def main():
    result = InputBox(
            title="PromptBox shenanigans", 
            text="What Country are you from?:"
            )
    def ok():
        pass
      #  return print(f"{result}")

    def mult(i):
        with multiprocessing.Pool() as pool:
            pool.map(ok, i)
#int(f"Result = {result}")
if __name__ == "__main__":
    n = None
    start_time = time.time()
    main()
    duration = time.time() - start_time
    print(f"Duration {duration}")

