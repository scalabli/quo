#!/usr/bin/env python3

from quo.prompt import Prompt

session = Prompt(hide=True)

if __name__ == "__main__":
    session.prompt("Password: ")
