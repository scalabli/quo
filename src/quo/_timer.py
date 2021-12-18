"""
Timer context manager, only used in debug.

"""

import time
import typing
import contextlib


@contextlib.contextmanager
def timer(subject: str = "time") -> typing.Generator[None, None, None]:
    """print the elapsed time. (only used in debugging)"""
    start = time.time()
    yield
    elapsed = time.time() - start
    elapsed_ms = elapsed * 1000
    print(f"{subject} elapsed {elapsed_ms:.1f}ms")
