"""
Collection of reusable components for building full screen applications.

All of these widgets implement the ``__pt_container__`` method, which makes
them usable in any situation where we are expecting a `quo`
container object.
"""
from functools import partial
from typing import Callable, Generic, List, Optional, Sequence, Tuple, TypeVar, Union

from quo.console.current import get_app
from quo.completion.auto_suggest import AutoSuggest, DynamicAutoSuggest
from quo.buffer import Buffer, BufferAcceptHandler
from quo.completion import Completer, DynamicCompleter
from quo.document import Document
from quo.filters import (
    Condition,
    FilterOrBool,
    has_focus,
    is_done,
    is_true,
    to_filter,
)
from quo.text.core import (
    AnyFormattedText,
    StyleAndTextTuples,
    Template,
    to_formatted_text,
)
from quo.text.utils import fragment_list_to_text
from quo.history import History
from quo.keys.key_binding.key_bindings import Bind
from quo.layout.containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    DynamicContainer,
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
)
from quo.layout.controls import (
    BufferControl,
    FormattedTextControl,
    GetLinePrefixCallable,
)
from quo.keys.key_binding.key_bindings import Bind
from quo.layout.dimension import AnyDimension
from quo.layout.dimension import Dimension as D
from quo.layout.dimension import to_dimension
from quo.layout.margin import ConditionalMargin, NumberedMargin, ScrollbarMargin
from quo.layout.processors import (
    AppendAutoSuggestion,
    BeforeInput,
    ConditionalProcessor,
    PasswordProcessor,
    Processor,
)
from quo.highlight.core import DynamicLexer, Lexer
from quo.mouse_events import MouseEvent, MouseEventType
from quo.utils.utils import get_width as get_cwidth
from quo.types import DynamicValidator, Validator

from .toolbars import SearchToolbar

__all__ = [
    "TextArea",
    "Label",
    "Button",
    "Frame",
    "Shadow",
    "Box",
    "VerticalLine",
    "HorizontalLine",
    "RadioList",
    "CheckboxList",
    "Checkbox",  # backward compatibility
    "ProgressBar",
]

# E = KeyPressEvent


class Border:
    "Box drawing characters."

    HORIZONTAL = "\u2501"
    # "\u2501" #2593
    VERTICAL = "\u2503" #"\u2593"
    # "\u2503"
    TOP_LEFT = "\u256D"
    TOP_RIGHT = "\u256E"
    BOTTOM_LEFT = "\u2570"
    BOTTOM_RIGHT = "\u256F"


class TextArea:
    """
    A simple input field.

    This is a higher level abstraction on top of several other classes with
    sane defaults.

    This widget does have the most common options, but it does not intend to
    cover every single use case. For more configurations options, you can
    always build a text area manually, using a
    :class:`~quo.buffer.Buffer`,
    :class:`~quo.layout.BufferControl` and
    :class:`~quo.layout.Window`.

    Buffer attributes:

    :param text: The initial text.
    :param multiline: If True, allow multiline input.
    :param completer: :class:`~quo.ompletion.Completer` instance
        for auto completion.
    :param complete_while_typing: Boolean.
    :param accept_handler: Called when `Enter` is pressed (This should be a
        callable that takes a buffer as input).
    :param history: :class:`~quo.history.History` instance.
    :param auto_suggest: :class:`~quo.completion.auto_suggest.AutoSuggest`
        instance for input suggestions.

    BufferControl attributes:

    :param password: When `True`, display using asterisks.
    :param focusable: When `True`, allow this widget to receive the focus.
    :param focus_on_click: When `True`, focus after mouse click.
    :param input_processors: `None` or a list of
        :class:`~quo.layout.Processor` objects.
    :param validator: `None` or a :class:`~quo.types.Validator`
        object.

    Window attributes:

    :param highlighter: :class:`~quo.lexers.Lexer` instance for syntax
        highlighting.
    :param wrap_lines: When `True`, don't scroll horizontally, but wrap lines.
    :param width: Window width. (:class:`~quo.layout.Dimension` object.)
    :param height: Window height. (:class:`~quo.layout.Dimension` object.)
    :param scrollbar: When `True`, display a scroll bar.
    :param style: A style string.
    :param fixed_width: When `True`, don't take up more width then the
                              preferred width reported by the control.
    :param fixed_height: When `True`, don't take up more width then the
                               preferred height reported by the control.
    :param get_line_prefix: None or a callable that returns formatted text to
        be inserted before a line. It takes a line number (int) and a
        wrap_count and returns formatted text. This can be used for
        implementation of line continuations, things like Vim "breakindent" and
        so on.

    Other attributes:

    :param search_field: An optional `SearchToolbar` object.
    """

    def __init__(
        self,
        text: str = "",
        multiline: FilterOrBool = False,
        hide: FilterOrBool = False,
        highlighter: Optional[Lexer] = None,
        auto_suggest: Optional[AutoSuggest] = None,
        completer: Optional[Completer] = None,
        complete_while_typing: FilterOrBool = True,
        type: Optional[Validator] = None,
        accept_handler: Optional[BufferAcceptHandler] = None,
        history: Optional[History] = None,
        focusable: FilterOrBool = True,
        focus_on_click: FilterOrBool = False,
        wrap_lines: FilterOrBool = True,
        read_only: FilterOrBool = False,
        width: AnyDimension = None,
        height: AnyDimension = None,
        extend_height: FilterOrBool = False,  # True,
        extend_width: FilterOrBool = True,
        fixed_height: FilterOrBool = False,
        fixed_width: FilterOrBool = False,
        line_numbers: bool = False,
        get_line_prefix: Optional[GetLinePrefixCallable] = None,
        scrollbar: bool = False,
        style: str = "",
        search_field: Optional[SearchToolbar] = None,
        preview_search: FilterOrBool = True,
        prompt: AnyFormattedText = "",
        input_processors: Optional[List[Processor]] = None,
    ) -> None:

        if search_field is None:
            search_control = None
        elif isinstance(search_field, SearchToolbar):
            search_control = search_field.control

        if input_processors is None:
            input_processors = []

        # Writeable attributes.
        self.completer = completer
        self.complete_while_typing = complete_while_typing
        self.highlighter = highlighter
        self.auto_suggest = auto_suggest
        self.read_only = read_only
        self.wrap_lines = wrap_lines
        self.type = type

        self.buffer = Buffer(
            document=Document(text, 0),
            multiline=multiline,
            read_only=Condition(lambda: is_true(self.read_only)),
            completer=DynamicCompleter(lambda: self.completer),
            complete_while_typing=Condition(
                lambda: is_true(self.complete_while_typing)
            ),
            type=DynamicValidator(lambda: self.type),
            auto_suggest=DynamicAutoSuggest(lambda: self.auto_suggest),
            accept_handler=accept_handler,
            history=history,
        )

        self.control = BufferControl(
            buffer=self.buffer,
            highlighter=DynamicLexer(lambda: self.highlighter),
            input_processors=[
                ConditionalProcessor(
                    AppendAutoSuggestion(), has_focus(self.buffer) & ~is_done
                ),
                ConditionalProcessor(
                    processor=PasswordProcessor(), filter=to_filter(hide)
                ),
                BeforeInput(prompt, style="class:text-area.prompt"),
            ]
            + input_processors,
            search_buffer_control=search_control,
            preview_search=preview_search,
            focusable=focusable,
            focus_on_click=focus_on_click,
        )

        if multiline:
            if scrollbar:
                right_margins = [ScrollbarMargin(display_arrows=True)]
            else:
                right_margins = []
            if line_numbers:
                left_margins = [NumberedMargin()]
            else:
                left_margins = []
        else:
            height = D.exact(1)
            left_margins = []
            right_margins = []

        style = "class:text-area " + style

        # If no height was given, guarantee height of at least 1.
        if height is None:
            height = D(min=1)

        self.window = Window(
            height=height,
            width=width,
            fixed_height=fixed_height,
            fixed_width=fixed_width,
            content=self.control,
            style=style,
            wrap_lines=Condition(lambda: is_true(self.wrap_lines)),
            left_margins=left_margins,
            right_margins=right_margins,
            get_line_prefix=get_line_prefix,
        )

    @property
    def text(self) -> str:
        """
        The `Buffer` text.
        """
        return self.buffer.text

    @text.setter
    def text(self, value: str) -> None:
        self.document = Document(value, 0)

    @property
    def document(self) -> Document:
        """
        The `Buffer` document (text + cursor position).
        """
        return self.buffer.document

    @document.setter
    def document(self, value: Document) -> None:
        self.buffer.set_document(value, bypass_readonly=True)

    @property
    def accept_handler(self) -> Optional[BufferAcceptHandler]:
        """
        The accept handler. Called when the user accepts the input.
        """
        return self.buffer.accept_handler

    @accept_handler.setter
    def accept_handler(self, value: BufferAcceptHandler) -> None:
        self.buffer.accept_handler = value

    def __pt_container__(self) -> Container:
        return self.window


class Label:
    """
    Widget that displays the given text. It is not editable or focusable.

    :param text: Text to display. Can be multiline. All value types accepted by
        :class:`quo.layout.FormattedTextControl` are allowed,
        including a callable.
    :param bold: Bold text.
    :param italic: Italic text.
    :param underline: Underline text.
    :param fg: Foreground text color.
    :param bg: Background text color.
    :param width: When given, use this width, rather than calculating it from
        the text size.
    :param fixed_width: When `True`, don't take up more width than
                              preferred, i.e. the length of the longest line of
                              the text, or value of `width` parameter, if
                              given. `True` by default
    :param fixed_height: When `True`, don't take up more width than the
                               preferred height, i.e. the number of lines of
                               the text. `False` by default.
    """

    def __init__(
        self,
        text: AnyFormattedText,
        style: str = "",
        fg: str = "",
        bg: str = "",
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        width: AnyDimension = None,
        fixed_height: bool = True,
        fixed_width: bool = False,
    ) -> None:

        self.text = text

        if fg and bg != "":
            setStyle = " fg:" + fg + " bg:" + bg
        elif fg != "" and bg == "":
            setStyle = " fg:" + fg
        elif fg == "" and bg != "":
            setStyle = " bg:" + bg

        else:
            setStyle = ""

        if italic:
            setStyle+=" italic"
        if bold:
            setStyle+=" bold"
        if underline:
            setStyle+=" underline"

        def get_width() -> AnyDimension:
            if width is None:
                text_fragments = to_formatted_text(self.text)
                text = fragment_list_to_text(text_fragments)
                if text:
                    longest_line = max(get_cwidth(line) for line in text.splitlines())
                else:
                    return D(preferred=0)
                return D(preferred=longest_line)
            else:
                return width

        self.formatted_text_control = FormattedTextControl(text=lambda: self.text)

        

        self.window = Window(
            content=self.formatted_text_control,
            width=get_width,
            height=D(min=1),
            style="class:label " + setStyle,
            fixed_height=fixed_height,
            fixed_width=fixed_width,
        )

    def __pt_container__(self) -> Container:
        return self.window


class Button:
    """
    Clickable button.

    :param text: The caption for the button.
    :param handler: `None` or callable. Called when the button is clicked. No
        parameters are passed to this callable. Use for instance Python's
        `functools.partial` to pass parameters to this callable if needed.
    :param width: Width of the button.
    """

    def __init__(
        self,
        text: str,
        handler: Optional[Callable[[], None]] = None,
        width: int = 12,
        left_symbol: str = None, #"«\u27EC",
        right_symbol: str = None, #"\u27ED»",
    ) -> None:

        self.text = text
        self.left_symbol = left_symbol
        self.right_symbol = right_symbol
        self.handler = handler
        self.width = width
        self.control = FormattedTextControl(
            self._get_text_fragments,
            bind=self._get_key_bindings(),
            focusable=True,
        )
        from quo.accordance import WIN

        if WIN:
            self.left_symbol="«["
            self.right_symbol="]»"
        else:
            self.left_symbol="«\u27EC"
            self.right_symbol="\u27ED»"

        def get_style() -> str:
            if get_app().layout.has_focus(self):
                return "class:button.focused"
            else:
                return "class:button"

        # Note: `fixed_width` is False, because we want to allow buttons
        #       to take more space if the parent container provides more space.
        #       Otherwise, we will also truncate the text.
        #       Probably we need a better way here to adjust to width of the
        #       button to the text.

        self.window = Window(
            self.control,
            align="center",
            height=1,
            width=width,
            style=get_style,
            fixed_width=False,
            fixed_height=True,
        )

    def _get_text_fragments(self) -> StyleAndTextTuples:
        width = self.width - (
            get_cwidth(self.left_symbol) + get_cwidth(self.right_symbol)
        )
        text = ("{{:^{}}}".format(width)).format(self.text)

        def handler(mouse_event: MouseEvent) -> None:
            if (
                self.handler is not None
                and mouse_event.event_type == MouseEventType.MOUSE_UP
            ):
                self.handler()

        return [
            ("class:button.arrow", self.left_symbol, handler),
            ("[SetCursorPosition]", ""),
            ("class:button.text", text, handler),
            ("class:button.arrow", self.right_symbol, handler),
        ]

    def _get_key_bindings(self) -> Bind:
        "Key bindings for the Button."
        from quo.event import Event

        kb = Bind()

        @kb.add(" ")
        @kb.add("enter")
        def _(event: Event) -> None:
            if self.handler is not None:
                self.handler()

        return kb

    def __pt_container__(self) -> Container:
        return self.window


class Frame:
    """
    Draw a border around any container, optionally with a title text.

    Changing the title and body of the frame is possible at runtime by
    assigning to the `body` and `title` attributes of this class.

    :param body: Another container object.
    :param title: Text to be displayed in the top of the frame (can be formatted text i.e <red>Hello</red>).
    :param frame_color: Frame color Style string to be applied to this widget.
    """

    from quo.keys.key_binding.key_bindings import Bind

    def __init__(
        self,
        body: AnyContainer,
        title: AnyFormattedText = "",
        frame_color: str = None,
        style: str = "",
        width: AnyDimension = None,
        height: AnyDimension = None,
        bind: Optional[Bind] = None,
        modal: bool = False,
        ) -> None:
        from quo.text.html import Text

        self.title = Text(title)
        self.body = body



        fill = partial(Window, style="class:frame.border" if frame_color is None else "fg:"+frame_color)
        style = "class:frame " + style

        top_row_with_title = VSplit(
            [
                fill(width=1, height=1, char=Border.TOP_LEFT),
                fill(char=Border.HORIZONTAL),
                fill(width=1, height=1, char="\u2563"),
                # Notice: we use `Template` here, because `self.title` can be an
                # `quo.text.Text` object for instance.
                Label(
                    lambda: Template(" {} ").format(self.title),
                 #   style="class:frame.label",
                    fixed_width=True,
                ),
                fill(width=1, height=1, char="\u2560"),
                fill(char=Border.HORIZONTAL),
                fill(width=1, height=1, char=Border.TOP_RIGHT),
            ],
            height=1,
        )

        top_row_without_title = VSplit(
            [
                fill(width=1, height=1, char=Border.TOP_LEFT),
                fill(char=Border.HORIZONTAL),
                fill(width=1, height=1, char=Border.TOP_RIGHT),
            ],
            height=1,
        )

        @Condition
        def has_title() -> bool:
            return bool(self.title)

        self.container = HSplit(
            [
                ConditionalContainer(content=top_row_with_title, filter=has_title),
                ConditionalContainer(content=top_row_without_title, filter=~has_title),
                VSplit(
                    [
                        fill(width=1, char=Border.VERTICAL),
                        DynamicContainer(lambda: self.body),
                        fill(width=1, char=Border.VERTICAL),
                        # Padding is required to make sure that if the content is
                        # too small, the right frame border is still aligned.
                    ],
                    padding=0,
                ),
                VSplit(
                    [
                        fill(width=1, height=1, char=Border.BOTTOM_LEFT),
                        fill(char=Border.HORIZONTAL),
                        fill(width=1, height=1, char=Border.BOTTOM_RIGHT),
                    ],
                    # specifying height here will increase the rendering speed.
                    height=1,
                ),
            ],
            width=width,
            height=height,
            style=style,
            bind=bind,
            modal=modal,
        )

    def __pt_container__(self) -> Container:
        return self.container


class Shadow:
    """
    Draw a shadow underneath/behind this container.
    (This applies `class:shadow` the the cells under the shadow. The Style
    should define the colors for the shadow.)

    :param body: Another container object.
    """

    def __init__(self, body: AnyContainer) -> None:
        self.container = FloatContainer(
            content=body,
            floats=[
                Float(
                    bottom=-1,
                    height=1,
                    left=1,
                    right=-1,
                    transparent=True,
                    content=Window(style="class:shadow"),
                ),
                Float(
                    bottom=-1,
                    top=1,
                    width=1,
                    right=-1,
                    transparent=True,
                    content=Window(style="class:shadow"),
                ),
            ],
        )

    def __pt_container__(self) -> Container:
        return self.container


class Box:
    """
    Add padding around a container.

    This also makes sure that the parent can provide more space than required by
    the child. This is very useful when wrapping a small element with a fixed
    size into a ``VSplit`` or ``HSplit`` object. The ``HSplit`` and ``VSplit``
    try to make sure to adapt respectively the width and height, possibly
    shrinking other elements. Wrapping something in a ``Box`` makes it flexible.

    :param body: Another container object.
    :param padding: The margin to be used around the body. This can be
        overridden by `padding_left`, padding_right`, `padding_top` and
        `padding_bottom`.
    :param style: A style string.
    :param char: Character to be used for filling the space around the body.
        (This is supposed to be a character with a terminal width of 1.)
    """

    from quo.keys.key_binding.key_bindings import Bind

    def __init__(
        self,
        body: AnyContainer,
        padding: AnyDimension = None,
        padding_left: AnyDimension = None,
        padding_right: AnyDimension = None,
        padding_top: AnyDimension = None,
        padding_bottom: AnyDimension = None,
        width: AnyDimension = None,
        height: AnyDimension = None,
        bg: str = "",
        style: str = "",
        char: Union[None, str, Callable[[], str]] = None,
        modal: bool = False,
        bind: Optional[Bind] = None,
    ) -> None:

        if padding is None:
            padding = D(preferred=0)

        def get(value: AnyDimension) -> D:
            if value is None:
                value = padding
            return to_dimension(value)

        self.padding_left = get(padding_left)
        self.padding_right = get(padding_right)
        self.padding_top = get(padding_top)
        self.padding_bottom = get(padding_bottom)
        self.body = body

        if bg != "":
            setStyle = " bg:" + bg
        else:
            setStyle = ""

        self.container = HSplit(
            [
                Window(height=self.padding_top, char=char),
                VSplit(
                    [
                        Window(width=self.padding_left, char=char),
                        body,
                        Window(width=self.padding_right, char=char),
                    ]
                ),
                Window(height=self.padding_bottom, char=char),
            ],
            width=width,
            height=height,
            style=setStyle,
            modal=modal,
            bind=None,
        )

    def __pt_container__(self) -> Container:
        return self.container


_T = TypeVar("_T")


class _DialogList(Generic[_T]):
    """
    Common code for `RadioList` and `CheckboxList`.
    """

    open_character: str = ""
    close_character: str = ""
    container_style: str = ""
    default_style: str = ""
    selected_style: str = ""
    checked_style: str = ""
    multiple_selection: bool = False
    show_scrollbar: bool = True

    def __init__(self, values: Sequence[Tuple[_T, AnyFormattedText]]) -> None:
        from quo.event import Event
        from quo.keys.key_binding.key_bindings import Bind
        from quo.keys.list import Keys

        assert len(values) > 0

        self.values = values
        # current_values will be used in multiple_selection,
        # current_value will be used otherwise.
        self.current_values: List[_T] = []
        self.current_value: _T = values[0][0]
        self._selected_index = 0

        # Key bindings.
        kb = Bind()

        @kb.add("up")
        def _up(event: Event) -> None:
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add("down")
        def _down(event: Event) -> None:
            self._selected_index = min(len(self.values) - 1, self._selected_index + 1)

        @kb.add("pageup")
        def _pageup(event: Event) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = max(
                    0, self._selected_index - len(w.render_info.displayed_lines)
                )

        @kb.add("pagedown")
        def _pagedown(event: Event) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = min(
                    len(self.values) - 1,
                    self._selected_index + len(w.render_info.displayed_lines),
                )

        @kb.add("enter")
        @kb.add(" ") #space bar
        def _click(event: Event) -> None:
            self._handle_enter()

        @kb.add(Keys.Any)
        def _find(event: Event) -> None:
            # We first check values after the selected value, then all values.
            values = list(self.values)
            for value in values[self._selected_index + 1 :] + values:
                text = fragment_list_to_text(to_formatted_text(value[1])).lower()

                if text.startswith(event.data.lower()):
                    self._selected_index = self.values.index(value)
                    return

        # Control and window.
        self.control = FormattedTextControl(
            self._get_text_fragments, bind=kb, focusable=True
        )

        self.window = Window(
            content=self.control,
            style=self.container_style,
            right_margins=[
                ConditionalMargin(
                    margin=ScrollbarMargin(display_arrows=True),
                    filter=Condition(lambda: self.show_scrollbar),
                ),
            ],
            fixed_height=True,
        )

    def _handle_enter(self) -> None:
        if self.multiple_selection:
            val = self.values[self._selected_index][0]
            if val in self.current_values:
                self.current_values.remove(val)
            else:
                self.current_values.append(val)
        else:
            self.current_value = self.values[self._selected_index][0]

    def _get_text_fragments(self) -> StyleAndTextTuples:
        def mouse_handler(mouse_event: MouseEvent) -> None:
            """
            Set `_selected_index` and `current_value` according to the y
            position of the mouse click event.
            """
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self._selected_index = mouse_event.position.y
                self._handle_enter()

        result: StyleAndTextTuples = []
        for i, value in enumerate(self.values):
            if self.multiple_selection:
                checked = value[0] in self.current_values
            else:
                checked = value[0] == self.current_value
            selected = i == self._selected_index

            style = ""
            if checked:
                style += " " + self.checked_style
            if selected:
                style += " " + self.selected_style

            result.append((style, self.open_character))

            if selected:
                result.append(("[SetCursorPosition]", ""))

            if checked:
                result.append((style, "*"))
            else:
                result.append((style, " "))

            result.append((style, self.close_character))
            result.append((self.default_style, " "))
            result.extend(to_formatted_text(value[1], style=self.default_style))
            result.append(("", "\n"))

        # Add mouse handler to all fragments.
        for i in range(len(result)):
            result[i] = (result[i][0], result[i][1], mouse_handler)

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self) -> Container:
        return self.window


class RadioList(_DialogList[_T]):
    """
    List of radio buttons. Only one can be checked at the same time.

    :param values: List of (value, label) tuples.
    """

    open_character = "("
    close_character = ")"
    container_style = "class:radio-list"
    default_style = "class:radio"
    selected_style = "class:radio-selected"
    checked_style = "class:radio-checked"
    multiple_selection = False


class CheckboxList(_DialogList[_T]):
    """
    List of checkbox buttons. Several can be checked at the same time.

    :param values: List of (value, label) tuples.
    """

    open_character = "["
    close_character = "]"
    container_style = "class:checkbox-list"
    default_style = "class:checkbox"
    selected_style = "class:checkbox-selected"
    checked_style = "class:checkbox-checked"
    multiple_selection = True


class Checkbox(CheckboxList[str]):
    """Backward compatibility util: creates a 1-sized CheckboxList

    :param text: the text
    """

    show_scrollbar = False

    def __init__(self, text: AnyFormattedText = "", checked: bool = False) -> None:
        values = [("value", text)]
        CheckboxList.__init__(self, values)
        self.checked = checked

    @property
    def checked(self) -> bool:
        return "value" in self.current_values

    @checked.setter
    def checked(self, value: bool) -> None:
        if value:
            self.current_values = ["value"]
        else:
            self.current_values = []


class VerticalLine(object):
    """
    A simple vertical line with a width of 1.
    """

    def __init__(self) -> None:
        self.window = Window(
            char=Border.VERTICAL, style="class:line,vertical-line", width=1
        )

    def __pt_container__(self) -> Container:
        return self.window


class HorizontalLine:
    """
    A simple horizontal line with a height of 1.
    """

    def __init__(self) -> None:
        self.window = Window(
            char=Border.HORIZONTAL, style="class:line,horizontal-line", height=1
        )

    def __pt_container__(self) -> Container:
        return self.window


class ProgressBar:
    def __init__(self) -> None:
        self._percentage = 60

        self.label = Label("60%")
        self.container = FloatContainer(
            content=Window(height=1),
            floats=[
                # We first draw the label, then the actual progress bar.  Right
                # now, this is the only way to have the colors of the progress
                # bar appear on top of the label. The problem is that our label
                # can't be part of any `Window` below.
                Float(content=self.label, top=0, bottom=0),
                Float(
                    left=0,
                    top=0,
                    right=0,
                    bottom=0,
                    content=VSplit(
                        [
                            Window(
                                style="class:progress-bar.used",
                                width=lambda: D(weight=int(self._percentage)),
                            ),
                            Window(
                                style="class:progress-bar",
                                width=lambda: D(weight=int(100 - self._percentage)),
                            ),
                        ]
                    ),
                ),
            ],
        )

    @property
    def percentage(self) -> int:
        return self._percentage

    @percentage.setter
    def percentage(self, value: int) -> None:
        self._percentage = value
        self.label.text = "{0}%".format(value)

    def __pt_container__(self) -> Container:
        return self.container

