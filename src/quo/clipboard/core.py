"""
Clipboard for command line interface.
"""
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional

from quo.selection import SelectionType

__all__ = [
    "Clipboard",
    "Data",
    "DummyClipboard",
    "DynamicClipboard",
]


class Data:
    """
    Data captured by the clipboard.

    :param text: string
    :param type: :class:`~quo.selection.SelectionType`
    """

    def __init__(
        self, text: str = "", type: SelectionType = SelectionType.CHARACTERS
    ) -> None:

        self.text = text
        self.type = type


class Clipboard(metaclass=ABCMeta):
    """
    Abstract baseclass for clipboards.
    (An implementation can be in memory, it can share the X11 or Windows
    keyboard, or can be persistent.)
    """

    @abstractmethod
    def set_data(self, data: Data) -> None:
        """
        Set data to the clipboard.

        :param data: :class:`~.Data` instance.
        """

    def set_text(self, text: str) -> None:  # Not abstract.
        """
        Shortcut for setting plain text on clipboard.
        """
        self.set_data(Data(text))

    def rotate(self) -> None:
        """
        For Emacs mode, rotate the kill ring.
        """

    @abstractmethod
    def get_data(self) -> Data:
        """
        Return clipboard data.
        """


class DummyClipboard(Clipboard):
    """
    Clipboard implementation that doesn't remember anything.
    """

    def set_data(self, data: Data) -> None:
        pass

    def set_text(self, text: str) -> None:
        pass

    def rotate(self) -> None:
        pass

    def get_data(self) -> Data:
        return Data()


class DynamicClipboard(Clipboard):
    """
    Clipboard class that can dynamically returns any Clipboard.

    :param get_clipboard: Callable that returns a :class:`.Clipboard` instance.
    """

    def __init__(self, get_clipboard: Callable[[], Optional[Clipboard]]) -> None:
        self.get_clipboard = get_clipboard

    def _clipboard(self) -> Clipboard:
        return self.get_clipboard() or DummyClipboard()

    def set_data(self, data: Data) -> None:
        self._clipboard().set_data(data)

    def set_text(self, text: str) -> None:
        self._clipboard().set_text(text)

    def rotate(self) -> None:
        self._clipboard().rotate()

    def get_data(self) -> Data:
        return self._clipboard().get_data()
