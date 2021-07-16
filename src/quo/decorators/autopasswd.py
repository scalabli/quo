from quo.decorators import core

def autopasswd(*param_decls, **kwargs):
    """Add a ``--password`` option which prompts for a password, hiding
    input and asking to enter the value again for confirmation.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--password"``.
    :param kwargs: Extra arguments are passed to :func:`app`.
    
    Example::

    @quo.app('--password', prompt=True, autoconfirm=True,
              hide=True)
     def changeadmin(password):
     pass
    """

    if not param_decls:
        param_decls = ("--password",)

    kwargs.setdefault("prompt", True)
    kwargs.setdefault("autoconfirm", True)
    kwargs.setdefault("hide", True)
    return app(*param_decls, **kwargs)


