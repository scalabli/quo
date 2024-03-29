"""
Utility for running a prompt_toolkit application in an asyncssh server.
"""
import asyncio
import traceback
from typing import Awaitable, Callable, Optional, TextIO, cast

import asyncssh

from quo.application.current import AppSession, create_app_session
from quo.data_structures import Size
from quo.input import create_pipe_input
from quo.output.videoterminal import Vt100

__all__ = ["SSHSession", "SSHServer"]


class SSHSession(asyncssh.SSHServerSession):
    def __init__(self, interact: Callable[["SSHSession"], Awaitable[None]]) -> None:
        self.interact = interact
        self.interact_task: Optional[asyncio.Task[None]] = None
        self._chan = None
        self.app_session: Optional[AppSession] = None

        # PipInput object, for sending input in the CLI.
        # (This is something that we can use in the prompt_toolkit event loop,
        # but still write date in manually.)
        self._input = create_pipe_input()
        self._output = None

        # Output object. Don't render to the real stdout, but write everything
        # in the SSH channel.
        class Stdout:
            def write(s, data):
                try:
                    if self._chan is not None:
                        self._chan.write(data.replace("\n", "\r\n"))
                except BrokenPipeError:
                    pass  # Channel not open for sending.

            def isatty(s) -> bool:
                return True

            def flush(s):
                pass

            @property
            def encoding(s):
                return self._chan._orig_chan.get_encoding()[0]

        self.stdout = cast(TextIO, Stdout())

    def _get_size(self) -> Size:
        """
        Callable that returns the current `Size`, required by Vt100_Output.
        """
        if self._chan is None:
            return Size(rows=20, columns=79)
        else:
            width, height, pixwidth, pixheight = self._chan.get_terminal_size()
            return Size(rows=height, columns=width)

    def connection_made(self, chan):
        self._chan = chan

    def shell_requested(self) -> bool:
        return True

    def session_started(self) -> None:
        self.interact_task = asyncio.get_event_loop().create_task(self._interact())

    async def _interact(self) -> None:
        if self._chan is None:
            # Should not happen.
            raise Exception("`_interact` called before `connection_made`.")

        if hasattr(self._chan, "set_line_mode") and self._chan._editor is not None:
            # Disable the line editing provided by asyncssh. Prompt_toolkit
            # provides the line editing.
            self._chan.set_line_mode(False)

        term = self._chan.get_terminal_type()

        self._output = Vt100(self.stdout, self._get_size, term=term, write_binary=False)
        with create_app_session(input=self._input, output=self._output) as session:
            self.app_session = session
            try:
                await self.interact(self)
            except BaseException:
                traceback.print_exc()
            finally:
                # Close the connection.
                self._chan.close()
                self._input.close()

    def terminal_size_changed(
        self, width: int, height: int, pixwidth, pixheight
    ) -> None:
        # Send resize event to the current application.
        if self.app_session and self.app_session.app:
            self.app_session.app._on_resize()

    def data_received(self, data, datatype):
        self._input.send_text(data)


class SSHServer(asyncssh.SSHServer):
    """
    Run a Quo application over an asyncssh server.

    This takes one argument, an `interact` function, which is called for each
    connection. This should be an asynchronous function that runs the
    prompt_toolkit applications. This function runs in an `AppSession`, which
    means that we can have multiple UI interactions concurrently.

    Example usage:

    .. code:: python

        async def interact(ssh_session: QuoSSHSession) -> None:
            await yes_no_dialog("my title", "my text").run_async()

            prompt_session = PromptSession()
            text = await prompt_session.prompt_async("Type something: ")
            print_formatted_text('You said: ', text)

        server = QuoSSHServer(interact=interact)
        loop = get_event_loop()
        loop.run_until_complete(
            asyncssh.create_server(
                lambda: MySSHServer(interact),
                "",
                port,
                server_host_keys=["/etc/ssh/..."],
            )
        )
        loop.run_forever()
    """

    def __init__(self, interact: Callable[[SSHSession], Awaitable[None]]) -> None:
        self.interact = interact

    def begin_auth(self, username: str) -> bool:
        # No authentication.
        return False

    def session_requested(self) -> SSHSession:
        return SSHSession(self.interact)
