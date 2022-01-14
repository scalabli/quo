#!/usr/bin/env python
"""
Styled just like an apt-get installation.
"""
import time
import quo

from quo.progress import formatters

style = quo.styles.Style.add(
    {
        "label": "bg:#ffff00 #000000",
        "percentage": "bg:#ffff00 #000000",
        "current": "#448844",
        "bar": "",
    }
)


def main():
    custom_formatters = [
        formatters.Label(),
        formatters.Text(": [", style="class:percentage"),
        formatters.Percentage(),
        formatters.Text("]", style="class:percentage"),
        formatters.Text(" "),
        formatters.Bar(sym_a="#", sym_b="#", sym_c="."),
        formatters.Text("  "),
    ]

    with quo.ProgressBar(style=style, formatters=custom_formatters) as pb:
        for i in pb(range(1600), label="Installing"):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
