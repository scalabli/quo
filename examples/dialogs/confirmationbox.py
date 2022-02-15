#!/usr/bin/env python
from quo import echo, ConfirmationBox

"""Example of a confirmation window"""

result = ConfirmationBox(
        title="Yes/No example",
        text="Do you want to confirm?").run()

echo(f"Result = {result}")

