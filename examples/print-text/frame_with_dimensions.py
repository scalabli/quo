import quo

@quo.command()
@quo.app("@frame", help="Print a frame")

def _frame(frame):
    """ Example of a simple layout """

    content = quo.widgets.TextArea(text="Hel
lo world🌍")
    quo.container(
            quo.widgets.Frame(
                content),
                height=2,                                   width=2,
                )
            

if __name__ == "__main__":
    import time
    s  = time.perf_counter()
    _frame()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
~
~
