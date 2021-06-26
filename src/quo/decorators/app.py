def app(*param_decls, **attrs):
    """Attaches an app to the command.  All positional arguments are
    passed as parameter declarations to :class:`App`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`App` instance manually
    and attaching it to the :attr:`Command.params` list.

    :param cls: the app class to instantiate.  This defaults to
                :class:`App`.
    """

    def decorator(f):
        # Issue 926, copy attrs, so pre-defined apps can re-use the same cls=
        app_attrs = attrs.copy()

        if "help" in app_attrs:
            app_attrs["help"] = inspect.cleandoc(app_attrs["help"])
        OptionClass = app_attrs.pop("class", App)
        _param_memo(f, OptionClass(param_decls, **app_attrs))
        return f

    return decorator

