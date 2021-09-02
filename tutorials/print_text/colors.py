from quo import command, echo

ansi_colors = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "vblack",
    "vred",
    "vgreen",
    "vyellow",
    "vblue",
    "vmagenta",
    "vcyan",
    "vwhite",
)


@command()
def cli():
    """This script prints some colors. It will also automatically remove
    all ANSI styles if data is piped into a file.

    Give it a try!
    """
    for color in ansi_colors:
        echo(f"I am colored {color}", fg=color)
    for color in ansi_colors:
        echo(f"I am colored {color} and bold", fg=color, bold=True)
    for color in ansi_colors:
        echo(f"I am reverse colored {color}", fg=color, reverse=True)

    echo("I am blinking", blink=True)
    echo(f"I am underlined", underline=True)
    echo(f"I am italicised", italic=True)


if __name__ == "__main__":
    cli()
