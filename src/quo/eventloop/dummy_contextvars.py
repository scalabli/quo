"""
Dummy contextvars implementation, to make quo work on Python 3.6.

As long as there is only one application running at a time, we don't need the
real contextvars. So, stuff like the telnet-server and so on requires 3.7.
"""
import typing as ty


def copy_context() -> "Context":
    return Context()


_T = ty.TypeVar("_T")


class Context:
    def run(self, callable: ty.Callable[..., _T], *args: ty.Any, **kwargs: ty.Any) -> _T:
        return callable(*args, **kwargs)

    def copy(self) -> "Context":
        return self


class Token(ty.Generic[_T]):
    pass


class ContextVar(ty.Generic[_T]):
    def __init__(self, name: str, *, default: ty.Optional[_T] = None) -> None:
        self._name = name
        self._value = default

    @property
    def name(self) -> str:
        return self._name

    def get(self, default: ty.Optional[_T] = None) -> _T:
        result = self._value or default
        if result is None:
            raise LookupError
        return result

    def set(self, value: _T) -> Token[_T]:
        self._value = value
        return Token()

    def reset(self, token: Token[_T]) -> None:
        pass
