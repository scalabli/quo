from json import loads, dumps
from typing import Any

from quo.text.text import Text
from .highlighter import JSONHighlighter, NullHighlighter


class JSON:
    """A renderable which pretty prints JSON.

    Args:
        json (str): JSON encoded data.
        indent (int, optional): Number of characters to indent by. Defaults to 2.
        highlight (bool, optional): Enable highlighting. Defaults to True.
    """

    def __init__(self, json: str, indent: int = 2, highlight: bool = True) -> None:
        data = loads(json)
        json = dumps(data, indent=indent)
        highlighter = JSONHighlighter() if highlight else NullHighlighter()
        self.text = highlighter(json)
        self.text.no_wrap = True
        self.text.overflow = None

    @classmethod
    def from_data(cls, data: Any, indent: int = 2, highlight: bool = True) -> "JSON":
        """Encodes a JSON object from arbitrary data.

        Returns:
            Args:
                data (Any): An object that may be encoded in to JSON
                indent (int, optional): Number of characters to indent by. Defaults to 2.
                highlight (bool, optional): Enable highlighting. Defaults to True.
        """
        json_instance: "JSON" = cls.__new__(cls)
        json = dumps(data, indent=indent)
        highlighter = JSONHighlighter() if highlight else NullHighlighter()
        json_instance.text = highlighter(json)
        json_instance.text.no_wrap = True
        json_instance.text.overflow = None
        return json_instance

    def __rich__(self) -> Text:
        return self.text
