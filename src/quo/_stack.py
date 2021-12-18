import typing

T = typing.TypeVar("T")


class Stack(typing.List[T]):
    """A small shim over builtin list."""

    @property
    def top(self) -> T:
        """Get top of stack."""
        return self[-1]

    def push(self, item: T) -> None:
        """Push an item on to the stack (append in stack nomenclature)."""
        self.append(item)
