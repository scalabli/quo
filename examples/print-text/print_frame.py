#!/usr/bin/env python
"""
Example usage of 'container', a tool to print
any layout in a non-interactive way.
"""
import quo

@quo.command()
@quo.app("--frame", help="Print a frame")

def _frame(frame):
    """ Example of a simple layout
    """
    content = quo.widgets.TextArea(text="Hello world🌍")
    quo.container(
        quo.widgets.Frame(
            content,
            title="Quo: python🐍")
        )

if __name__ == "__main__":
    import time
    s  = time.perf_counter()
    _frame()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
