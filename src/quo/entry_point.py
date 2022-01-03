import quo

from quo.i_o import echo
from quo.color.rgb import *
cli = quo.echo(f"sjsjjdjd", fg="red")
quo.command()
quo.app("@start")
def maijj(start):
    echo(f"* ", fg="red", nl=False)
    echo(f"Support for ANSI and RGB color models")
    echo(f"* ", fg="blue", nl=False)
    echo(f"Support for tabular presentation of data")
    echo(f"* ", fg="green", nl=False)
    echo(f"Interactive progressbars")
    echo(f"* ", fg="magenta", nl=False)
    echo(f"Code completions")
    echo(f"* ", fg="yellow", nl=False)
    echo(f"Nesting of commands")
    echo(f"* ", fg=teal, nl=False)
    echo(f"Automatic help page generation")
    echo(f"* ", fg=aquamarine, nl=False)
    echo(f"Highlighting")
    echo(f"* ", fg=khaki, nl=False)
    echo(f"Lightweight")
import sys
def main(as_module=False):
    # TODO omit sys.argv once https://githu.com/pallets/click/issues/536 is fixed
    cli.main(args=sys.argv[1:], prog_name="python3 -m quo" if as_module else None)

if __name__ == "__main__":                      main(as_module=True)
#if __name__ == "__main__":
#    main()

