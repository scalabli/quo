import collections
import typing

CacheKey = typing.TypeVar("CacheKey")
CacheValue = typing.TypeVar("CacheValue")


class LRUCache(typing.Generic[CacheKey, CacheValue], collections.OrderedDict):  # type: ignore # https://github.com/python/mypy/issues/6904
    """
    A dictionary-like container that stores a given maximum items.

    If an additional item is added when the LRUCache is full, the least
    recently used key is discarded to make room for the new item.

    """

    def __init__(self, cache_size: int) -> None:
        self.cache_size = cache_size
        super(LRUCache, self).__init__()

    def __setitem__(self, key: CacheKey, value: CacheValue) -> None:
        """Store a new views, potentially discarding an old value."""
        if key not in self:
            if len(self) >= self.cache_size:
                self.popitem(last=False)
        collections.OrderedDict.__setitem__(self, key, value)

    def __getitem__(self: typing.Dict[CacheKey, CacheValue], key: CacheKey) -> CacheValue:
        """Gets the item, but also makes it most recent."""
        value: CacheValue = collections.OrderedDict.__getitem__(self, key)
        collections.OrderedDict.__delitem__(self, key)
        collections.OrderedDict.__setitem__(self, key, value)
        return value
