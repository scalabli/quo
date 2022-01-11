#!/usr/bin/env python
"""
Demonstration of all the ANSI colors.
"""
import quo

@quo.command()
@quo.app("--ansi")
def main(ansi):
    wide_space = ("", "       ")
    space = ("", " ")

    quo.inscribe(quo.text.HTML("\n<u>Foreground colors</u>"))
    quo.inscribe(
        quo.text.FormattedText(
            [
                ("ansiblack", "ansiblack"),
                wide_space,
                ("ansired", "ansired"),
                wide_space,
                ("ansigreen", "ansigreen"),
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

    quo.inscribe(quo.text.HTML("\n<u>Background colors</u>"))
    quo.inscribe(
        quo.text.FormattedText(
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
    quo.inscribe()


if __name__ == "__main__":
    main()
