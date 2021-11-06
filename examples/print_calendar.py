"""
Builds calendar layout using Columns and Tables.
Usage:
python print_calendar.py [YEAR]
Example:
python print_calendar.py 2021
"""
import argparse
import calendar
from datetime import datetime

from quo.align import Align
from quo import box
from quo.columns import Columns
from quo.console import Console
from quo.table import Table
from quo.text import Text


def print_calendar(year):
    """Print a calendar for a given year."""

    today = datetime.today()
    year = int(year)
    cal = calendar.Calendar()
    today_tuple = today.day, today.month, today.year

    tables = []

    for month in range(1, 13):
        table = Table(
            title=f"{calendar.month_name[month]} {year}",
            style="green",
            box=box.SIMPLE_HEAVY,
            padding=0,
        )

        for week_day in cal.iterweekdays():
            table.column(
                "{:.3}".format(calendar.day_name[week_day]), position="right"
            )

        month_days = cal.monthdayscalendar(year, month)
        for weekdays in month_days:
            days = []
            for index, day in enumerate(weekdays):
                day_label = Text(str(day or ""), style="magenta")
                if index in (5, 6):
                    day_label.stylize("blue")
                if day and (day, month, year) == today_tuple:
                    day_label.stylize("white on dark_red")
                days.append(day_label)
            table.row(*days)

        tables.append(Align.center(table))

    console = Console()
    columns = Columns(tables, padding=1, expand=True)
    console.rule(str(year))
    console.echo()
    console.echo(columns)
    console.rule(str(year))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rich calendar")
    parser.add_argument("year", metavar="year", type=int)
    args = parser.parse_args()

    print_calendar(args.year)
