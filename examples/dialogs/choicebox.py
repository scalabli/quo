#!/usr/bin/env python
"""
Example of button dialog window.
"""

import quo


def main():
    result = quo.ChoiceBox(
        title="ChoiceBox example",
        text="Are you sure?",
        buttons=[("Yes", True), ("No", False), ("Maybe...", None)],
    ).run()

    quo.echo(f"Result = {result}")


if __name__ == "__main__":
    main()
