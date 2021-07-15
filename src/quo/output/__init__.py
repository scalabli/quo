from .core import DummyOutput
from .core import Output
from .color import ColorDepth
#rom .generator import pager
#from .inscribe import echo
from .defaults import create_output
#from .vitals import flair
#from .vitals import interpose
#from .vitals import style
#from .vitals import unstyle


__all__ = [
    # Base.
    "Output",
    "DummyOutput",
    # Color depth.
    "ColorDepth",
    # Defaults.
    "create_output",
]
