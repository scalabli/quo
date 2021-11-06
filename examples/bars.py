"""

Use Bar to renderer a sort-of circle.

"""
import math

from quo.align import Align
from quo.bar import Bar
from quo.color.color import Color
from quo import evoke


SIZE = 40

for row in range(SIZE):
    y = (row / (SIZE - 1)) * 2 - 1
    x = math.sqrt(1 - y * y)
    color = Color.from_rgb((1 + y) * 127.5, 0, 0)
    bar = Bar(2, width=SIZE * 2, begin=1 - x, end=1 + x, color=color)
    evoke(Align.center(bar))
