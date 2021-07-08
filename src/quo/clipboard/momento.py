from collections import deque
from typing import Deque, Optional

from .core import Clipboard, Data

__all__ = [
    "InMemoryClipboard",
]


class InMemoryClipboard(Clipboard):
    """
    Default clipboard implementation.
    Just keep the data in memory.

    This implements a kill-ring, for Emacs mode.
    """

    def __init__(
        self, data: Optional[Data] = None, max_size: int = 60
    ) -> None:

        assert max_size >= 1

        self.max_size = max_size
        self._ring: Deque[Data] = deque()

        if data is not None:
            self.set_data(data)

    def set_data(self, data: Data) -> None:
        self._ring.appendleft(data)

        while len(self._ring) > self.max_size:
            self._ring.pop()

    def get_data(self) -> Data:
        if self._ring:
            return self._ring[0]
        else:
            return Data()

    def rotate(self) -> None:
        if self._ring:
            # Add the very first item at the end.
            self._ring.append(self._ring.popleft())
