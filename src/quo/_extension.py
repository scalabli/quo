import typing

def load_ipython_extension(ip: typing.Any) -> None:  # pragma: no cover
    # prevent circular import
    from quo.pretty import install
    from quo.traceback import install as tr_install

    install()
    tr_install()
