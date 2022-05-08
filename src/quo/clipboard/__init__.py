#from .core import Clipboard, Data, DummyClipboard, DynamicClipboard #Data DummyClipboard, Clipboard
from .momento import InMemoryClipboard

from .pyperclip import PyperClipboard

__all__ = [
    "Clipboard",
    "ClipboardData",
    "DummyClipboard",
    "DynamicClipboard",
    "InMemoryClipboard",
]
