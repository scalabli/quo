#!/usr/bin/env python
"""
Example of a placeholer that's displayed as long as no input is given.
"""
import quo

if __name__ == "__main__":
    answer = quo.Suite(
        "Give me some input: ",
        placeholder=quo.HTML('<style color="#888888">(please type something)</style>'),
    )
    print("You said: %s" % answer)
