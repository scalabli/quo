#!/usr/bin/env python
"""
Simple example of input validation.
"""

from quo import echo, confirm, prompt, command, app, flair
#from quo.shortcuts import elicit
#from quo.validation import Validator

@command()
@app("--email", prompt="Enter e-mail address")
def validate(email):
    return "@" in email
#   return
#else:
#    flair(f"Not a valid email", fg="red", bg="white")



#prompt("Enter e-mail address")
#return "@" 

#def is_valid_email(text):
 #   return "@" in text


#validator = Validator.from_callable(
#    is_valid_email,
#    error_message="Not a valid e-mail address (Does not contain an @).",
#    move_cursor_to_end=True,
#)


#def main():
    # Validate when pressing ENTER.
 #   text = elicit(
 #       "Enter e-mail address: ", validator=validator, #validate_while_typing=False
 #   )
#    print("You said: %s" % text)

    # While typing
#    text = elicit(
 #       "Enter e-mail address: ", validator=validator,# validate_while_typing=True
#    )
#    print("You said: %s" % text)


if __name__ == "__main__":
    validate()
