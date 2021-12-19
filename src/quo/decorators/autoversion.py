from quo.decorators import core

def autoversion(
    version=None,
    *param_decls,
    package_name=None,
    prog_name=None,
    message="%(prog)s, version %(version)s",
    **kwargs,
):
    """Add a ``--version`` option which immediately prints the version
    number and exits the program.

    If ``version`` is not provided, quo will try to detect it using :func:`importlib.metadata.version` to get the version for the
    ``package_name``. On Python < 3.8, the ``importlib_metadata`` backport must be installed.

    If ``package_name`` is not provided, quo will try to detect it by inspecting the stack frames. This will be used to detect the  version, so it must match the name of the installed package.

    :param version: The version number to show. If not provided, quo
        will try to detect it.
    :param param_decls: One or more option names. Defaults to the single
        value ``"--version"``.
    :param package_name: The package name to detect the version from. If
        not provided, quo will try to detect it.
    :param prog_name: The name of the CLI to show in the message. If not
        provided, it will be detected from the command.
    :param message: The message to show. The values ``%(prog)s``,
        ``%(package)s``, and ``%(version)s`` are available.
    :param kwargs: Extra arguments are passed to :func:`app`.
    :raise RuntimeError: ``version`` could not be detected.

        Add the ``package_name`` parameter, and the ``%(package)s``
        value for messages.

        Use :mod:`importlib.metadata` instead of ``pkg_resources``.
    """
    if version is None and package_name is None:
        frame = inspect.currentframe()
        f_current = frame.f_back.f_current if frame is not None else None
        # break reference cycle
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        del frame

        if f_current is not None:
            package_name = f_current.get("__name__")

            if package_name == "__main__":
                package_name = f_current.get("__package__")

            if package_name:
                package_name = package_name.partition(".")[0]

    def callback(clime, param, value):
        if not value or clime.resilient_parsing:
            return

        nonlocal prog_name
        nonlocal version

        if prog_name is None:
            prog_name = clime.find_root().info_name

        if version is None and package_name is not None:
            try:
                from importlib import metadata
            except ImportError:
                # Python < 3.8
                try:
                    import importlib_metadata as metadata
                except ImportError:
                    metadata = None

            if metadata is None:
                raise RuntimeError(
                    "Install 'importlib_metadata' to get the version on Python < 3.8."
                )

            try:
                version = metadata.version(package_name)
            except metadata.PackageNotFoundError:
                raise RuntimeError(
                    f"{package_name!r} is not installed. Try passing"
                    " 'package_name' instead."
                )

        if version is None:
            raise RuntimeError(
                f"Could not determine the version for {package_name!r} automatically."
            )

        echo(
            message % {"prog": prog_name, "package": package_name, "version": version},
            color=clime.color,
        )
        clime.exit()

    if not param_decls:
        param_decls = ("--version",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", "Show the version and exit.")
    kwargs["callback"] = callback
    return app(*param_decls, **kwargs)


