#!/usr/bin/env python
"""
Example of an input box dialog.
"""

import quo


def main():
    result = quo.PromptBox(
        title="PromptBox shenanigans", text="What Country are you from?:"
    ).run()

    quo.echo("Result = {result}")


if __name__ == "__main__":
    main()
