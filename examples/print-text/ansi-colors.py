#!/usr/bin/env python
"""
Demonstration of all the ANSI colors.
"""
from quo import print
from quo.text import Text, FormattedText

wide_space = ("", "       ")
space = ("", " ")

print(Text("\n<u>Foreground colors</u>"))
print(FormattedText([
    ("black", "black"),
    wide_space,
    ("red", "red"),
    wide_space,
    ("green", "green"),
    wide_space,
    ("ansiyellow", "ansiyellow"),
    wide_space,
    ("ansiblue", "ansiblue"),
    wide_space,
    ("ansimagenta", "ansimagenta"),
    wide_space,
    ("ansicyan", "ansicyan"),
    wide_space,
    ("ansigray", "ansigray"),
    wide_space,
    ("", "\n"),
                ("ansibrightblack", "ansibrightblack"),
                space,
                ("ansibrightred", "ansibrightred"),
                space,
                ("ansibrightgreen", "ansibrightgreen"),
                space,
                ("ansibrightyellow", "ansibrightyellow"),
                space,
                ("ansibrightblue", "ansibrightblue"),
                space,
                ("ansibrightmagenta", "ansibrightmagenta"),
                space,
                ("ansibrightcyan", "ansibrightcyan"),
                space,
                ("ansiwhite", "ansiwhite"),
                space,
            ]
        )
    )

print(Text("\n<u>Background colors</u>"))
print(
    FormattedText(
            [
                ("bg:ansiblack ansiwhite", "ansiblack"),
                wide_space,
                ("bg:ansired", "ansired"),
                wide_space,
                ("bg:ansigreen", "ansigreen"),
                wide_space,
                ("bg:ansiyellow", "ansiyellow"),
                wide_space,
                ("bg:ansiblue ansiwhite", "ansiblue"),
                wide_space,
                ("bg:ansimagenta", "ansimagenta"),
                wide_space,
                ("bg:ansicyan", "ansicyan"),
                wide_space,
                ("bg:ansigray", "ansigray"),
                wide_space,
                ("", "\n"),
                ("bg:ansibrightblack", "ansibrightblack"),
                space,
                ("bg:ansibrightred", "ansibrightred"),
                space,
                ("bg:ansibrightgreen", "ansibrightgreen"),
                space,
                ("bg:ansibrightyellow", "ansibrightyellow"),
                space,
                ("bg:ansibrightblue", "ansibrightblue"),
                space,
                ("bg:ansibrightmagenta", "ansibrightmagenta"),
                space,
                ("bg:ansibrightcyan", "ansibrightcyan"),
                space,
                ("bg:ansiwhite", "ansiwhite"),
                space,
            ]
        )
    )
print()


