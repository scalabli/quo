#!/usr/bin/env python3
"""
Demonstration of how to print using ANSI colors
"""
from quo import echo



def main():
    echo(f"SPECIAL FORMATING", bold=True, fg="red", underline=True)

    echo(f"  Bold  ", bold=True)
    echo(f"  Dim  ", dim=True)
    echo(f"  Reverse  ", reverse=True)
    echo(f"  Underline  ", underline=True)
    echo(f"  Blink  ", blink=True)
    echo(f"  Italic ", italic=True)

    # Ansi colors.
    echo(f"ANSI FOREGROUND COLORS", bold=True, fg="red", underline=True)

    echo(f"  RED   ", fg="red")
    echo(f"  BLUE  ", fg="blue")
    echo(f"  YELLOW  ", fg="yellow")

    # Other named colors.

    echo(f"NON-ANSI COLORS", bold=True,fg="red", underline=True)
    echo(f"  TEAL  ", fg=(0, 128, 128))
    echo(f"  BROWN  ", fg=(165, 42, 42))
    echo(f"  INDIGO  ", fg=(75, 0, 130))


    # Background colors.
    echo(f"ANSI BACKGROUND COLORS", fg="red", underline=True, bold=True)
    echo(f"  CYAN  ", bg="cyan")
    echo(f"  MAGENTA  ", bg="magenta")
    echo(f"  GREEN  ", bg="green")



if __name__ == "__main__":
    main()
