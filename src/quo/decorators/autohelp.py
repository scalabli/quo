from quo.decorators import core
def autohelp(*param_decls, **kwargs):
    """Add a ``--help`` option which immediately prints the help page
    and exits the program.

    This is usually unnecessary, as the ``--help`` option is added to each command automatically unless ``add_autohelp=False`` is passed.

    :param param_decls: One or more option names. Defaults to the single  value ``"--help"``.
    :param kwargs: Extra arguments are passed to :func:`app`.
    """

    def callback(clime, param, value):
        if not value or clime.resilient_parsing:
            return

        echo(clime.get_help(), color=clime.color)
        clime.exit()

    if not param_decls:
        param_decls = ("--help",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", "Show this message and exit.")
    kwargs["callback"] = callback
    return app(*param_decls, **kwargs)
