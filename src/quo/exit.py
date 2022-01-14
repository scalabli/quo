import os
import sys

def quick_exit(code: int):

    """Low-level exit that skips Python's cleanup
but speeds up exit by about 10ms for things like shell completion.
    :param code: Exit code.
    """
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)
