#!/usr/bin/env python
"""
Example of a call to `prompt` with a default value.
The input is pre-filled, but the user can still edit the default.
"""
import getpass
from quo import prompt, echo

name = getpass.getuser()

prompt("What is your name?")
echo(f"Your default name is {name}")
