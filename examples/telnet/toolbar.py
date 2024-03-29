#!/usr/bin/env python
"""
Example of a telnet application that displays a bottom toolbar and completions
in the prompt.
"""
import logging

from quo.completion import WordCompleter
from quo.contrib.telnet.server import TelnetServer
from asyncio import get_event_loop
from quo.shortcuts import Prompt

# Set up logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def interact(connection):
    # When a client is connected, erase the screen from the client and say
    # Hello.
    connection.send("Welcome!\n")

    # Display prompt with bottom toolbar.
    animal_completer = WordCompleter(["alligator", "ant"])

    def get_toolbar():
        return "Bottom toolbar..."

    session = Prompt()
    result = await session.prompt_async(
        "Say something: ", bottom_toolbar=get_toolbar, completer=animal_completer
    )

    connection.send("You said: {}\n".format(result))
    connection.send("Bye.\n")


def main():
    server = TelnetServer(interact=interact, port=2323)
    server.start()
    get_event_loop().run_forever()


if __name__ == "__main__":
    main()
