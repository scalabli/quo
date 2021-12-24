#!/usr/bin/env python
import quo

session = quo.Prompt(is_password=True)

if __name__ == "__main__":
    password = session.prompt("Password: ")
    quo.echo("You said: %s" % password)
