#!/usr/bin/env python
"""
A progress bar that displays a formatted title above the progress bar and has a
colored label.
"""
import time
import quo

def main():
    title = quo.text.HTML('Downloading <style bg="yellow" fg="black">4 files...</style>')
    label = quo.text.HTML("<ansired>some file</ansired>: ")

    with quo.ProgressBar(title=title) as pb:
        for i in pb(range(800), label=label):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
