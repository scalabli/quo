#!/usr/bin/env python
import quo

session = quo.Prompt()
if __name__ == "__main__":
    print(
        "This is multiline input. press [Meta+Enter] or [Esc] followed by [Enter] to accept input."
    )
    print("You can click with the mouse in order to select text.")
    answer = session.prompt("Multiline input: ", multiline=True, mouse_support=True)
    print("You said: %s" % answer)
