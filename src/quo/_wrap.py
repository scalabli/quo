import re
import typing

from .cells import cell_len, chop_cells
from ._loop import loop_last

re_word = re.compile(r"\s*\S+\s*")


def words(text: str) -> typing.Iterable[typing.Tuple[int, int, str]]:
    position = 0
    word_match = re_word.match(text, position)
    while word_match is not None:
        start, end = word_match.span()
        word = word_match.group(0)
        yield start, end, word
        word_match = re_word.match(text, end)


def divide_line(text: str, width: int, fold: bool = True) -> typing.List[int]:
    divides: typing.List[int] = []
    append = divides.append
    line_position = 0
    _cell_len = cell_len
    for start, _end, word in words(text):
        word_length = _cell_len(word.rstrip())
        if line_position + word_length > width:
            if word_length > width:
                if fold:
                    for last, line in loop_last(
                        chop_cells(word, width, position=line_position)
                    ):
                        if last:
                            line_position = _cell_len(line)
                        else:
                            start += len(line)
                            append(start)
                else:
                    if start:
                        append(start)
                    line_position = _cell_len(word)
            elif line_position and start:
                append(start)
                line_position = _cell_len(word)
        else:
            line_position += _cell_len(word)
    return divides

