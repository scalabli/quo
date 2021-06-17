def scrollable(
    text_or_generator: t.Union[t.Iterable[str], t.Callable[[], t.Iterable[str]], str],
    color: t.Optional[bool] = None,
) -> None:
    """This function takes a text and shows it via an environment specific
    pager on stdout.


    :param text_or_generator: the text to page, or alternatively, a
                              generator emitting the text to page.
    :param color: controls if the pager supports ANSI colors or not.  The
                  default is autodetection.
    """
    color = resolve_color_default(color)

    if inspect.isgeneratorfunction(text_or_generator):
        i = t.cast(t.Callable[[], t.Iterable[str]], text_or_generator)()
    elif isinstance(text_or_generator, str):
        i = [text_or_generator]
    else:
        i = iter(t.cast(t.Iterable[str], text_or_generator))

    # convert every element of i to a text type if necessary
    text_generator = (el if isinstance(el, str) else str(el) for el in i)

    from quo.implementation import pager

    return pager(itertools.chain(text_generator, "\n"), color)
