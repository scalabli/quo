#!/usr/bin/env python
"""
Example of a confirmation prompt.
"""
import quo

if __name__ == "__main__":
    answer = quo.confirm("Should we do that?")
    print("You said: %s" % answer)
