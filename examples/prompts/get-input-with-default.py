#!/usr/bin/env python
"""
Example of a call to `Prompt` with a default value.
The input is pre-filled, but the user can still edit the default.
"""
import getpass
import quo

session = quo.Prompt()


if __name__ == "__main__":
    answer = session.prompt("What is your name: ", default=getpass.getuser()))
    print(f"You said: {nswer}")
