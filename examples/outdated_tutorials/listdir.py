"""
A very simple `ls` clone.

If your terminal supports hyperlinks you should be able to launch files by clicking the filename
(usually with cmd / ctrl).

"""

import os
import sys

from quo import echo, Console
from quo.columns import Columns
from quo.text import Text
con = Console()
try:
    root_path = sys.argv[1]
except IndexError:
    echo("Usage: python listdir.py DIRECTORY")
else:

    def make_filename_text(filename):
        path = os.path.abspath(os.path.join(root_path, filename))
        text = Text(filename, style="bold blue" if os.path.isdir(path) else "default")
        text.stylize(f"link file://{path}")
        text.highlight_regex(r"\..*?$", "bold")
        return text

    filenames = [
        filename for filename in os.listdir(root_path) if not filename.startswith(".")
    ]
    filenames.sort(key=lambda filename: filename.lower())
    filename_text = [make_filename_text(filename) for filename in filenames]
    columns = Columns(filename_text, equal=True, column_first=True)
    con.echo(columns)
