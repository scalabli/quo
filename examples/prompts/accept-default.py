#!/usr/bin/env python
"""
Example of `accept_default`, a way to automatically accept the input that the
user typed without allowing him/her to edit it.

This should display the prompt with all the formatting like usual, but not
allow any editing.
"""
import quo

session = quo.Prompt(
       # accept_default=True,
        #default="test"
        )



if __name__ == "__main__":
    answer = session.prompt(
        quo.text.HTML("<b>Type <u>some input</u>: </b>"), accept_default=True, default= "test")

    quo.echo(f"You said: {answer}")
