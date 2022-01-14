#!/usr/bin/env python3

import quo

session = quo.Prompt()

if __name__ == "__main__":
    print("You have Vi keybindings here. Press [Esc] to go to navigation mode.")
    answer = session.prompt("Give me some input: ", multiline=False, vi_mode=True)
    print(f"You said: {answer}")
