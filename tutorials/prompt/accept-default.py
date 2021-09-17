#!/usr/bin/env python
"""
Accept default
"""

from quo import prompt, echo

answer = prompt("Type some input", default="python")

echo(f"You said: {answer}")
