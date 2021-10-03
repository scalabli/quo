#!/usr/bin/env python
"""
Example of a placeholer that's displayed as long as no input is given.
"""
from quo import Elicit, echo
from quo.widgets.placeholder import *

s = Elicit()

answer = s.elicit("Gimme some input: ", placeholder=cyan)

echo(f"You said: {answer}")

