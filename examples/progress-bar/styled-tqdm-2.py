#!/usr/bin/env python
"""
Styled similar to tqdm, another progress bar impl
"""
import quo
import time

style = quo.styles.Style.add({"bar-a": "reverse"})


def main():
    custom_formatters = [
        quo.progress.formatters.Label(suffix=": "),
        quo.progress.formatters.Percentage(),
        quo.progress.formatters.Bar(start="|", end="|", sym_a=" ", sym_b=" ", sym_c=" "),
        quo.progress.formatters.Text(" "),
        quo.progress.formatters.Progress(),
        quo.progress.formatters.Text(" ["),
        quo.progress.formatters.TimeElapsed(),
        quo.progress.formatters.Text("<"),
        quo.progress.formatters.TimeLeft(),
        quo.progress.formatters.Text(", "),
        quo.progress.formatters.IterationsPerSecond(),
        quo.progress.formatters.Text("it/s]"),
    ]

    with quo.ProgressBar(style=style, formatters=custom_formatters) as pb:
        for i in pb(range(1600), label="Installing"):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
