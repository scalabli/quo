#!/usr/bin/env python
from quo import Elicit, echo

echo(f"This is multiline input. press [Meta+Enter] or [Esc] followed by [Enter] to accept input.")
echo(f"You can click with the mouse in order to select text.")

s = Elicit()

answer = s.elicit("Multiline input: ", multiline=True, mouse_support=True)
echo(f"You said: {answer}")



