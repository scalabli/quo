from .core import DummyInput
from .core import Input
#from .vitals import prompt
from .defaults import create_input, create_pipe_input

__all__ = [
    # Base.
    "Input",
    "DummyInput",
    # Defaults.
    "create_input",
    "create_pipe_input",
]
