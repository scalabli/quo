#!/usr/bin/env python
"""
Example of a telnet application that displays a dialog window.
"""
import logging
import asyncio

import quo


from quo.shortcuts.dialogs import confirmation

# Set up logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def interact(connection):
    result = await confirmation(
        title="Yes/no dialog demo", text="Press yes or no"
    ).run_async()

    connection.send("You said: {}\n".format(result))
    connection.send("Bye.\n")


def main():
    server = quo.contrib.telnet.TelnetServer(interact=interact, port=2323)
    server.start()
    ayncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
