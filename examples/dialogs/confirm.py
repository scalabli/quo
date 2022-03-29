#!/usr/bin/env python
from quo import echo
from quo.dialog import ConfirmBox
"""Example of a confirmation window"""

result = ConfirmBox(
        title="Yes/No example",
        text="Do you want to confirm?")
#echo(f"Result = {result}")

