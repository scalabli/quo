#!/usr/bin/env python

import quo

session = quo.Prompt()

@quo.command()
@quo.app("@prompt")
def main(prompt):
    quo.echo("(1/3) If you press meta-! or esc-! at the following prompt, you can enter system commands.")

    answer = session.prompt("Give me some input: ", enable_system_elicit=True)
    quo.echo(f"You said: {answer}")

    # Enable suspend.
    quo.echo("(2/3) If you press Control-Z, the application will suspend.")
    answer = session.prompt("Give me some input: ", enable_suspend=True)
    quo.echo(f"You said: {answer}")

    # Enable open_in_editor
    quo.echo("(3/3) If you press Control-X Control-E, the prompt will open in $EDITOR.")
    answer = session.prompt("Give me some input: ", enable_open_in_editor=True)
    quo.echo(f"You said: {answer}")

if __name__ == "__main__":
    main()
