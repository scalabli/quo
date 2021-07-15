#!/usr/bin/env python
"""
Demonstration of how to print using ANSI escape sequences.
This is cross platform.
"""
from quo import flair, echo



def main():
    flair(f"SPECIAL FORMATING", bold=True, fg="red", underline=True, dim=True)
    flair(f"  Bold  ", bold=True)
    flair(f"  Dim  ", dim=True)
    flair(f"  Reverse  ", reverse=True)
    flair(f"  Underline  ", underline=True)
    flair(f"  Blink  ", blink=True)
   # print(ANSI("    \x1b[1mBold"))
  #  print(ANSI("    \x1b[6mBlink"))
 #   print(ANSI("    \x1b[3mItalic"))
  #  print(ANSI("    \x1b[7mReverse"))
 #   print(ANSI("    \x1b[4mUnderline"))
  #  print(ANSI("    \x1b[8mHidden\x1b[0m (Hidden)"))

    # Ansi colors.
 #   title("ANSI colors")

 #   print(ANSI("    \x1b[91mANSI Red"))
 #   print(ANSI("    \x1b[94mANSI Blue"))

    # Other named colors.
#    title("Named colors")

 #   print(ANSI("    \x1b[38;5;214morange"))
 #   print(ANSI("    \x1b[38;5;90mpurple"))

    # Background colors.
 #   title("Background colors")

#    print(ANSI("    \x1b[97;101mANSI Red"))
#    print(ANSI("    \x1b[97;104mANSI Blue"))

    print()


if __name__ == "__main__":
    main()
