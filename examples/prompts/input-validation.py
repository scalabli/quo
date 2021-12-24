#!/usr/bin/env python
"""
Simple example of input validation.
"""
import quo

session = quo.Prompt()

def is_valid_email(text):
    return "@" in text


validator = quo.types.Validator.from_callable(
    is_valid_email,
    error_message="Not a valid e-mail address (Does not contain an @).",
    move_cursor_to_end=True,
)


def main():
    # Validate when pressing ENTER.
    text = session.prompt(
        "Enter e-mail address: ", validator=validator, validate_while_typing=False
    )
    print("You said: %s" % text)

    # While typing
    text = session.prompt(
        "Enter e-mail address: ", validator=validator, validate_while_typing=True
    )
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
