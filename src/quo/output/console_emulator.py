from typing import Any, Optional, TextIO

from quo.data_structures import Size

from .core import Output
from .color import ColorDepth
from .videoterminal import Vt100
from .win32 import Win32Output

__all__ = [
    "ConEmu",
]


class ConEmu:
    """
    ConEmu (short for Console emulator) is a free and open-source tabbed terminal emulator for Windows. ConEmu presents multiple consoles and simple GUI applications as one customizable GUI window with tabs and a status bar. It also provides emulation for ANSI escape codes for color, bypassing the capabilities of the standard Windows Console Host to provide 256 and 24-bit color. This output class serves as a proxy to both `Win32Output` and `Vt100`. It uses `Win32Output` for console sizing and scrolling, but all cursor movements and scrolling happens through the `Vt100`.

    """

    def __init__(
        self, stdout: TextIO, default_color_depth: Optional[ColorDepth] = None
    ) -> None:
        self.win32_output = Win32Output(stdout, default_color_depth=default_color_depth)
        self.vt100_output = Vt100_Output(
            stdout, lambda: Size(0, 0), default_color_depth=default_color_depth
        )

    @property
    def responds_to_cpr(self) -> bool:
        return False  # We don't need this on Windows.

    def __getattr__(self, name: str) -> Any:
        if name in (
            "get_size",
            "get_rows_below_cursor_position",
            "enable_mouse_support",
            "disable_mouse_support",
            "scroll_buffer_to_prompt",
            "get_win32_screen_buffer_info",
            "enable_bracketed_paste",
            "disable_bracketed_paste",
        ):
            return getattr(self.win32_output, name)
        else:
            return getattr(self.vt100_output, name)


Output.register(ConEmuOutput)
