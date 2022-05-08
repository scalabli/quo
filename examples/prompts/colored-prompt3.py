from quo.color import Color
from quo.prompt import Prompt

style = Color("fg:khaki")

session = Prompt(style=style)

message = [
        ("#cc2244", "T"),
        ("#bb4444", "r"),
        ("#996644", "u"),
        ("#cc8844", "e "),
        ("#ccaa44", "C"),
        ("#bbaa44", "o"),
        ("#99aa44", "l"),
        ("#778844", "o"),
        ("#55aa44", "r "),
        ("#33aa44", "p"),
        ("#11aa44", "r"),
        ("#11aa66", "o"),
        ("#11aa88", "m"),
        ("#11aaaa", "p"),
        ("#11aacc", "t"),
        ("#11aaee", ": ")
        ]

session.prompt(message)
