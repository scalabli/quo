#!/usr/bin/env python
import quo

def main():
    """Example of a confirmation window"""
    result = quo.ConfirmationBox(title="Yes/No example", text="Do you want to confirm?").run()

    quo.echo(f"Result = {result}")


if __name__ == "__main__":
    main()
