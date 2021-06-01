from .accordance import filename_to_ui
from .accordance import get_text_stderr
from .utilities import echo

from typing import Any, Dict, Optional, Sequence, Type



class FileError(QuoException):
    """Raised if a file cannot be opened."""

    def __init__(self, filename, hint=None):
        ui_filename = filename_to_ui(filename)
        if hint is None:
            hint = "unknown error"

        super().__init__(hint)
        self.ui_filename = ui_filename
        self.filename = filename

    def format_message(self):
        return f"Could not open file {self.ui_filename}: {self.message}"
