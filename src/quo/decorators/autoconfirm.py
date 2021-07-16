from quo.decorators import core
def autoconfirm(*param_decls, **kwargs):
    """Add a ``--yes`` option which shows a prompt before continuing if not passed. If the prompt is declined, the program will exit.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--yes"``.
    :param kwargs: Extra arguments are passed to :func:`app`.
    """

    def callback(clime, param, value):
        if not value:
            clime.abort()

    if not param_decls:
        param_decls = ("--yes",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("callback", callback)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("prompt", "Do you want to continue?")
    kwargs.setdefault("help", "Confirm the action without prompting.")
    return app(*param_decls, **kwargs)


