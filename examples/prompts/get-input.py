#!/usr/bin/env python
"""
The most simple prompt example.
"""

from quo import prompt, echo
#from prompt_toolkit import prompt

answer = prompt("Give me some input")
echo(f"You said: {answer}")
