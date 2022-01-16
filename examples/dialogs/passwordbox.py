#!/usr/bin/env python
"""
Example of an password input dialog.
"""
import quo

def main():
    result = quo.PromptBox(
        title="Password dialog example",
        text="Please type your password:",
        password=True,
    ).run()

    quo.echo(f"{result}")


if __name__ == "__main__":
    main()
