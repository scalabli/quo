#!/usr/bin/env python3

from quo.prompt import Prompt

session = Prompt(hide=True)

session.prompt("Password: ")
