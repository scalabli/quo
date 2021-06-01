
def autoconfirm(*param_decls, **kwargs):
    """Add a ``--yes`` option which shows a prompt before continuing if
    not passed. If the prompt is declined, the program will exit.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--yes"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def callback(ctx, param, value):
        if not value:
            ctx.abort()

    if not param_decls:
        param_decls = ("--yes",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("callback", callback)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("prompt", "Do you want to continue?")
    kwargs.setdefault("help", "Confirm the action without prompting.")
    return option(*param_decls, **kwargs)


