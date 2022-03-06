#!/usr/bin/env python

from quo import echo
from quo.console import app, command
from quo.prompt import Prompt

session = Prompt()

@command()
@app("--prompt")
def main(prompt):
    echo("(1/3) If you press meta-! or esc-! at the following prompt, you can enter system commands.")

    answer = session.prompt("Give me some input: ", system_prompt=True)
    echo(f"You said: {answer}")

    # Enable suspend.
    echo("(2/3) If you press Control-Z, the application will suspend.")
    answer = session.prompt("Give me some input: ", suspend=True)
    echo(f"You said: {answer}")

    # Enable open_in_editor
    echo("(3/3) If you press Control-X Control-E, the prompt will open in $EDITOR.")
    answer = session.prompt("Give me some input: ", enable_open_in_editor=True)
    echo(f"You said: {answer}")

if __name__ == "__main__":
    main()
