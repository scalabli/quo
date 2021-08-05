from quo.clipboard import copypaste
from quo.i_o import echo
import sys

if len(sys.argv) > 1 and sys.argv[1] in ('-c', '--copy'):
    if len(sys.argv) > 2:
        copypaste.copy(sys.argv[2])
    else:
        copypaste.copy(sys.stdin.read())
elif len(sys.argv) > 1 and sys.argv[1] in ('-p', '--paste'):
    sys.stdout.write(copypaste.paste())
else:
    echo('Usage: python -m pyperclip [-c | --copy] [text_to_copy] | [-p | --paste]')
    print()
    echo('If a text_to_copy argument is provided, it is copied to the')
    echo('clipboard. Otherwise, the stdin stream is copied to the')
    echo('clipboard. (If reading this in from the keyboard, press')
    echo('CTRL-Z on Windows or CTRL-D on Linux/macOS to stop.')
    echo('When pasting, the clipboard will be written to stdout.')
