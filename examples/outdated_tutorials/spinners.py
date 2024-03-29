from time import sleep

from quo.columns import Columns
from quo.panel import Panel
from quo.live import Live
from quo.text import Text
from quo.spinner import Spinner, SPINNERS

all_spinners = Columns(
    [
        Spinner(spinner_name, text=Text(repr(spinner_name), style="green"))

        for spinner_name in sorted(SPINNERS)
    ],
    column_first=True,
    expand=True,
)


with Live(
    Panel(all_spinners, title="Spinner", border_style="blue"),
    refresh_per_second=20,
) as live:
    while True:
        sleep(10)
