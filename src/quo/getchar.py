import warnings

from quo.expediency import inscribe


_interpose = None
def getchar(inscribe=False):
    warnings.warn(
            DeprecationWarning(                                       '"interpose" is deprecated and will be removed in Quo 2022.2, use "getchar" instead.'
            )
            )

    """Fetches a single character from the terminal and returns it.  This
    will always return a unicode character and under certain rare
    circumstances this might return more than one character.  The
    situations which more than one character is returned is when for
    whatever reason multiple characters end up in the terminal buffer or
    standard input was not actually a terminal.
    Note that this will always read from the terminal, even if something
    is piped into the standard input.
    Note for Windows: in rare cases when typing non-ASCII characters, this
    function might wait for a second character and then return both at once.
    This is because certain Unicode characters look like special-key markers.
    :param inscribe: if set to `True`, the character read will also show up on
                 the terminal.  The default is to not show it.
    """
    f = _interpose
    if f is None:
        from quo.implementation import interpose as f
    return f(inscribe)
