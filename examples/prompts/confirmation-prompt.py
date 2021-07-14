#!/usr/bin/env python
"""
Example of a confirmation prompt.
"""
from quo import confirm, echo

answer = confirm("Should we do that?")
echo(f"You said: {answer}")
