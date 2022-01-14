import quo


def print_version(
        clime: quo.Clime,
        param: quo.Parameter,
        value: bool
        ) -> None:
    if not value or clime.parse:
        return quo.echo("djdkd")

@quo.command()
@quo.app("--version",
        is_eager=True,
        callback=print_version,
        expose_value=False,
        is_flag = True
        )
def main(version):

    quo.echo("")

if __name__ == "__main__":
    main()

