#!/usr/bin/env python
"""
Example of the fancy ZSH prompt that @anki-code was using.

The theme is coming from the xonsh plugin from the xhh project:
https://github.com/xxh/xxh-plugin-xonsh-theme-bar

See:
- https://github.com/xonsh/xonsh/issues/3356
- https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1111
"""
import datetime
from quo.prompt import Prompt
import quo
session = Prompt()

from quo.text import (
    fragment_list_width,
    merge_formatted_text,
    to_formatted_text,
)

style = quo.style.Style.add(
    {
        "username": "#aaaaaa italic",
        "path": "#ffffff bold",
        "branch": "bg:#666666",
        "branch exclamation-mark": "#ff0000",
        "env": "bg:#666666",
        "left-part": "bg:#444444",
        "right-part": "bg:#444444",
        "padding": "bg:#444444",
    }
)


def get_prompt() -> quo.text.Text:
    """
    Build the prompt dynamically every time its rendered.
    """
    left_part = quo.text.Text(
        "<left-part>"
        " <username>root</username> "
        " abc "
        "<path>~/.oh-my-zsh/themes</path>"
        "</left-part>"
    )
    right_part = quo.text.Text(
        "<right-part> "
        "<branch> master<exclamation-mark>!</exclamation-mark> </branch> "
        " <env> py36 </env> "
        " <time>%s</time> "
        "</right-part>"
    ) % (datetime.datetime.now().isoformat(),)

    used_width = sum(
        [
            fragment_list_width(to_formatted_text(left_part)),
            fragment_list_width(to_formatted_text(right_part)),
        ]
    )

    total_width = quo.console.get_app().output.get_size().columns
    padding_size = total_width - used_width

    padding = quo.text.Text("<padding>%s</padding>") % (" " * padding_size,)

    return merge_formatted_text([left_part, padding, right_part, "\n", "# "])


def main() -> None:
    while True:
        answer = session.prompt(get_prompt, style=style, refresh_interval=1)
        print("You said: %s" % answer)


if __name__ == "__main__":
    main()
