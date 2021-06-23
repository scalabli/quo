def tether(name=None, **attrs):
    """Creates a new :class:`Tether` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Tether`.
    """
    attrs.setdefault("class", Tether)
    return command(name, **attrs)
