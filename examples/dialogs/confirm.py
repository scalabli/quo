#!/usr/bin/env python
from quo import print
from quo.dialog import ConfirmBox
"""Example of a confirmation window"""

result = ConfirmBox(
        title="Yes/No example",
        text="Do you want to confirm?",
        bg=False)
print(f"Result = {result}")

