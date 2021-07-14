#!/usr/bin/env python
"""
Demonstration of how the input can be indented.
"""
from quo.shortcuts import elicit

if __name__ == "__main__":
    answer = elicit(
        "Give me some input: (ESCAPE followed by ENTER to accept)\n > ", multiline=True
    )
    print("You said: %s" % answer)
