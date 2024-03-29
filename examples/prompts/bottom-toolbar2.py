#!/usr/bin/env python
"""
A few examples of displaying a bottom toolbar.

The ``Prompt`` function takes a ``bottom_toolbar`` attribute.
This can be any kind of formatted text (plain text, or HTML), or
it can be a callable that takes an App and returns an of these.

The bottom toolbar will always receive the style 'bottom-toolbar', and the text
inside will get 'bottom-toolbar.text'. These can be used to change the default
style.
"""
import time
from quo import echo
from quo.prompt import Prompt
from quo.style import Style
from quo.text import Text


session = Prompt()

def main():
    # Example 1: fixed text.
    text = session.prompt("Say something: ", bottom_toolbar="This is quo toolbar")
  #  echo(f"You said: {text}")

    # Example 2: fixed text from a callable:
    def get_toolbar():
        return "Bottom toolbar: time=%r" % time.time()

    text = session.prompt("Say something: ", bottom_toolbar=get_toolbar, refresh_interval=0.5)
   # echo(f"You said: {text}")

    # Example 3: Using HTML:
    text = session.prompt(
        "Say something: ",
        bottom_toolbar=Text( '(html) <b>This</b> <u>is</u> a <style bg="red">toolbar</style>'
        ),
    )
  #  echo(f"You said: {text}")


    # Example 4: styling differently.
    style = Style.add(
        {
            "bottom-toolbar": "#aaaa00 bg:#ff0000",
            "bottom-toolbar.text": "#aaaa44 bg:#aa4444",
        }
    )

    text = session.prompt("Say something: ", bottom_toolbar="This is a toolbar", style=style)
    print("You said: %s" % text)

    # Example 6: Using a list of tokens.
    def get_bottom_toolbar():
        return [
            ("", " "),
            ("bg:#ff0000 fg:#000000", "This"),
            ("", " is a "),
            ("bg:#ff0000 fg:#000000", "toolbar"),
            ("", ". "),
        ]

    text = session.prompt("Say something: ", bottom_toolbar=get_bottom_toolbar)
    print("You said: %s" % text)

    # Example 7: multiline fixed text.
    text = session.prompt("Say something: ", bottom_toolbar="This is\na multiline toolbar")
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
