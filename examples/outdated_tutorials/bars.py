"""

Use Bar to renderer a sort-of circle.

"""
import math
import quo

SIZE = 40
cc = quo.Console()
for row in range(SIZE):
    y = (row / (SIZE - 1)) * 2 - 1
    x = math.sqrt(1 - y * y)
    fg = quo.Color.from_rgb((1 + y) * 127.5, 0, 0)
    from quo.bar import Bar
    bar = Bar(2, width=SIZE * 2, begin=1 - x, end=1 + x, fg=fg)
    from quo.align import Align
    cc.echo(Align.center(bar))
