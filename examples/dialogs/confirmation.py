#!/usr/bin/env python
import quo

from quo.shortcuts import confirmation

@quo.command()
@quo.app("@dialog")
def main(dialog):
    """Example of a confirmation window"""
    result = confirmation(title="Yes/No dialog example", text="Do you want to confirm?").run()

    print("Result = {}".format(result))


if __name__ == "__main__":
    main()
