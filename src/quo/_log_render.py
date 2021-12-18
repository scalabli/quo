import typing
from datetime import datetime


from quo._text import Text

if typing.TYPE_CHECKING:
    from quo.console.console import Console, ConsoleRenderable, RenderableType
    from quo.table import Table

FormatTimeCallable = typing.Callable[[datetime], Text]

TextType = typing.Union[str, "Text"]

class LogRender:
    def __init__(
        self,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: typing.Union[str, FormatTimeCallable] = "[%x %X]",
        omit_repeated_times: bool = True,
        level_width: typing.Optional[int] = 8,
    ) -> None:
        self.show_time = show_time
        self.show_level = show_level
        self.show_path = show_path
        self.time_format = time_format
        self.omit_repeated_times = omit_repeated_times
        self.level_width = level_width
        self._last_time: typing.Optional[Text] = None

    def __call__(
        self,
        console: "Console",
        renderables: typing.Iterable["ConsoleRenderable"],
        log_time: typing.Optional[datetime] = None,
        time_format: typing.Optional[typing.Union[str, FormatTimeCallable]] = None,
        level: TextType = "",
        path: typing.Optional[str] = None,
        line_no: typing.Optional[int] = None,
        link_path: typing.Optional[str] = None,
    ) -> "Table":
        from .containers import Renderables
        from .table import Table

        output = Table.grid(padding=(0, 1))
        output.expand = True
        if self.show_time:
            output.add_column(style="log.time")
        if self.show_level:
            output.add_column(style="log.level", width=self.level_width)
        output.add_column(ratio=1, style="log.message", overflow="fold")
        if self.show_path and path:
            output.add_column(style="log.path")
        row: typing.List["RenderableType"] = []
        if self.show_time:
            log_time = log_time or console.get_datetime()
            time_format = time_format or self.time_format
            if callable(time_format):
                log_time_display = time_format(log_time)
            else:
                log_time_display = Text(log_time.strftime(time_format))
            if log_time_display == self._last_time and self.omit_repeated_times:
                row.append(Text(" " * len(log_time_display)))
            else:
                row.append(log_time_display)
                self._last_time = log_time_display
        if self.show_level:
            row.append(level)

        row.append(Renderables(renderables))
        if self.show_path and path:
            path_text = Text()
            path_text.append(
                path, style=f"link file://{link_path}" if link_path else ""
            )
            if line_no:
                path_text.append(f":{line_no}")
            row.append(path_text)

        output.add_row(*row)
        return output

