from abc import ABC


class RichRenderable(ABC):
    """An abstract base class for renderables.

    Note that there is no need to extend this class, the intended use is to check if an
    object supports the renderables. For example::

        if isinstance(my_object, RichRenderable):
            console.echo(my_object)

    """

    @classmethod
    def __subclasshook__(cls, other: type) -> bool:
        """Check if this class supports the render protocol."""
        return hasattr(other, "__rich_console__") or hasattr(other, "__rich__")


if __name__ == "__main__":  # pragma: no cover
    from quo.text.text import Text

    t = Text()
    print(isinstance(Text, RichRenderable))
    print(isinstance(t, RichRenderable))

    class Foo:
        pass

    f = Foo()
    print(isinstance(f, RichRenderable))
    print(isinstance("", RichRenderable))
