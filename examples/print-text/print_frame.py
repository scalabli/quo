#!/usr/bin/env python
"""
Example usage of 'container', a tool to print
any layout in a non-interactive way.
"""
import quo
@quo.command("frame")
@quo.app("--frames")
def _frame(frames):
    """ Example of a simple layout
    """
    content = quo.widget.TextArea(text="Hello world🌍")
    quo.container(
        quo.widget.Frame(
            content,
            title="Quo: python🐍")
        )

if __name__ == "__main__":
    import time
    s  = time.perf_counter()
    _frame()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
