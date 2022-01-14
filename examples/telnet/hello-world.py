#!/usr/bin/env python
"""
A simple Telnet application that asks for input and responds.

The interaction function is a quo coroutine.
Also see the `hello-world-asyncio.py` example which uses an asyncio coroutine.
That is probably the preferred way if you only need Python 3 support.
"""
import logging

import quo

from quo.contrib.telnet.server import TelnetServer
from asyncio import get_event_loop

session = quo.Prompt()



# Set up logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def interact(connection):
    quo.clear()
    connection.send("Welcome!\n")

    # Ask for input.
    result = await session.prompt(message="Say something: ", async_=True)

    # Send output.
    connection.send("You said: {}\n".format(result))
    connection.send("Bye.\n")


def main():
    server = TelnetServer(interact=interact, port=2323)
    server.start()
    get_event_loop().run_forever()


if __name__ == "__main__":
    main()
