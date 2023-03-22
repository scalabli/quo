from typing import Callable, List, Optional, Union, Tuple, Any, Iterable, cast
from quo.shortcuts.utils import container
from quo.layout.controls import UIControl, UIContent
from quo.layout.containers import Window
from quo.cache.core import SimpleCache
from quo.console.current import _current_app_session


OneStyleAndTextTuple = Union[
    Tuple[str, str], Tuple[str, str, None]
]

# List of (style, text) tuples.
StyleAndTextTuples = List[OneStyleAndTextTuple]

RichText = Union[
    str,
    StyleAndTextTuples,
    Callable[[], Any],
    None,
]

def getActiveApp():
    """
    Get the current active (running) Application.
    An :class:`.Console` is active during the
    :meth:`.Console.run_async` call.

    We assume that there can only be one :class:`.Console` active at the
    same time. There is only one terminal window, with only one stdin and
    stdout. This makes the code significantly easier than passing around the
    :class:`.Console` everywhere.

    """
    session = _current_app_session.get()
    if session.app is not None:
        return session.app



def split_lines(fragments: StyleAndTextTuples) -> Iterable[StyleAndTextTuples]:
    """
    Take a single list of (style_str, text) tuples and yield one such list for each
    line. Just like str.split, this will yield at least one item.

    :param fragments: List of (style_str, text) or (style_str, text, mouse_handler)
                      tuples.
    """
    line: StyleAndTextTuples = []

    for style, string, *mouse_handler in fragments:
        parts = string.split("\n")

        for part in parts[:-1]:
            if part:
                line.append(cast(OneStyleAndTextTuple, (style, part, *mouse_handler)))
            yield line
            line = []

        line.append(cast(OneStyleAndTextTuple, (style, parts[-1], *mouse_handler)))

    # Always yield the last line, even when this is an empty line. This ensures
    # that when `fragments` ends with a newline character, an additional empty
    # line is yielded. (Otherwise, there's no way to differentiate between the
    # cases where `fragments` does and doesn't end with a newline.)
    yield line



class FormattedText(StyleAndTextTuples):
    """
    A list of ``(style, text)`` tuples.

    (In some situations, this can also be ``(style, text, mouse_handler)``
    tuples.)
    """

    def __pt_formatted_text__(self) -> StyleAndTextTuples:
        return self

    def __repr__(self) -> str:
        return "FormattedText(%s)" % super().__repr__()

def convertToFormattedText(
    value: RichText, style: str = "", auto_convert: bool = False
) -> "FormattedText":
    """
    Convert the given value (which can be formatted text) into a list of text
    fragments. (Which is the canonical form of formatted text.) The outcome is
    always a `FormattedText` instance, which is a list of (style, text) tuples.

    It can take a plain text string, an `HTML` or `ANSI` object, anything that
    implements `__pt_formatted_text__` or a callable that takes no arguments and
    returns one of those.

    :param style: An additional style string which is applied to all text
        fragments.
    :param auto_convert: If `True`, also accept other types, and convert them
        to a string first.
    """
    result: Union[FormattedText, StyleAndTextTuples]

    if value is None:
        result = []
    elif isinstance(value, str):
        result = [("", value)]
    elif isinstance(value, list):
        result = value  # StyleAndTextTuples
    elif callable(value):
        return convertToFormattedText(value(), style=style)
    elif auto_convert:
        result = [("", "{}".format(value))]
   
    else:
        raise ValueError(
            "No formatted text. Expecting a unicode object, "
            "Text, ANSI or a FormattedText instance. Got %r" % (value,)
        )

    # Apply extra style.
    if style:
        result = cast(
            StyleAndTextTuples,
            [(style + " " + item_style, *rest) for item_style, *rest in result],
        )

    # Make sure the result is wrapped in a `FormattedText`. Among other
    # reasons, this is important for `print_formatted_text` to work correctly
    # and distinguish between lists and formatted text.
    if isinstance(result, FormattedText):
        return result
    else:
        return FormattedText(result)

class FormattedTextItem(UIControl):
    """
    Control that displays formatted text. This can be either plain text, an
    :class:`~quo.text.Text` object, a list of ``(style_str,
    text)`` tuples or a callable that takes no argument and returns one of
    those, depending on how you prefer to do the formatting. See
    ``quo.layout.formatted_text`` for more information.

    (It's mostly optimized for rather small widgets, like toolbars, menus, etc...)

    When this UI control has the focus, the cursor will be shown in the upper
    left corner of this control by default. There are two ways for specifying
    the cursor position:

    - Pass a `get_cursor_position` function which returns a `Point` instance
      with the current cursor position.

    - If the (formatted) text is passed as a list of ``(style, text)`` tuples
      and there is one that looks like ``('[SetCursorPosition]', '')``, then
      this will specify the cursor position.

    Mouse support:

        The list of fragments can also contain tuples of three items, looking like:
        (style_str, text, handler). When mouse support is enabled and the user
        clicks on this fragment, then the given handler is called. That handler
        should accept two inputs: (Application, MouseEvent) and it should
        either handle the event or return `NotImplemented` in case we want the
        containing Window to handle this event.



    :param text: Text or formatted text to be displayed.
    :param style: Style string applied to the content. (If you want to style
        the whole :class:`~quo.layout.Window`, pass the style to the
        :class:`~quo.layout.Window` instead.)
    :param get_cursor_position: A callable that returns the cursor position as
        a `Point` instance.
    """

    def __init__(
        self,
        text: RichText = "",
        style: str = "",
        modal: bool = False,
        get_cursor_position=None, #: Optional[Callable[[], Optional[Point]]] = None,
    ) -> None:

        self.text = text  # No type check on 'text'. This is done dynamically.
        self.style = style


        self.modal = modal
        self.get_cursor_position = get_cursor_position

        #: Cache for the content.
        self._content_cache: SimpleCache[Hashable, UIContent] = SimpleCache(maxsize=18)
        self._fragment_cache: SimpleCache[int, StyleAndTextTuples] = SimpleCache(maxsize=1)
        # Only cache one fragment list. We don't need the previous item.

        # Render info for the mouse support.
        self._fragments: Optional[StyleAndTextTuples] = None

    def reset(self) -> None:
        self._fragments = None


    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.text)

    def _get_formatted_text_cached(self) -> StyleAndTextTuples:
        """
        Get fragments, but only retrieve fragments once during one render run.
        (This function is called several times during one rendering, because
        we also need those for calculating the dimensions.)
        """
        return self._fragment_cache.get(
            getActiveApp().render_counter, lambda: convertToFormattedText(self.text, self.style)
        )

    def preferred_width(self, max_available_width: int) -> int:
        """
        Return the preferred width for this control.
        That is the width of the longest line.
        """
        text = fragment_list_to_text(self._get_formatted_text_cached())
        line_lengths = [get_cwidth(l) for l in text.split("\n")]
        return max(line_lengths)

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix,#: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:
        """
        Return the preferred height for this control.
        """
        content = self.create_content(width, None)
        if wrap_lines:
            height = 0
            for i in range(content.line_count):
                height += content.get_height_for_line(i, width, get_line_prefix)
                if height >= max_available_height:
                    return max_available_height
            return height
        else:
            return content.line_count

    def create_content(self, width: int, height: Optional[int]) -> UIContent:
        # Get fragments
        fragments_with_mouse_handlers = self._get_formatted_text_cached()
        fragment_lines_with_mouse_handlers = list(
            split_lines(fragments_with_mouse_handlers)
        )

        # Strip mouse handlers from fragments.
        fragment_lines: List[StyleAndTextTuples] = [
            [(item[0], item[1]) for item in line]
            for line in fragment_lines_with_mouse_handlers
        ]

        # Keep track of the fragments with mouse handler, for later use in
        # `mouse_handler`.
        self._fragments = fragments_with_mouse_handlers

        # If there is a `[SetCursorPosition]` in the fragment list, set the
        # cursor position here.
        def get_cursor_position(
            fragment: str = "[SetCursorPosition]",
        ):# -> Optional[Point]:
            for y, line in enumerate(fragment_lines):
                x = 0
                for style_str, text, *_ in line:
                    if fragment in style_str:
                        return Point(x=x, y=y)
                    x += len(text)
            return None

        # If there is a `[SetMenuPosition]`, set the menu over here.
        def get_menu_position():# -> Optional[Point]:
            return get_cursor_position("[SetMenuPosition]")

        cursor_position = (self.get_cursor_position or get_cursor_position)()

        # Create content, or take it from the cache.
        key = (tuple(fragments_with_mouse_handlers), width, cursor_position)

        def get_content() -> UIContent:
            return UIContent(
                get_line=lambda i: fragment_lines[i],
                line_count=len(fragment_lines),
                #show_cursor=self.show_cursor,
                cursor_position=cursor_position,
                menu_position=get_menu_position(),
            )

        return self._content_cache.get(key, get_content)

    def mouse_handler(self, mouse_event):# MouseEvent) -> "NotImplementedOrNone":
        """
        Handle mouse events.

        (When the fragment list contained mouse handlers and the user clicked on
        on any of these, the matching handler is called. This handler can still
        return `NotImplemented` in case we want the
        :class:`~quo.layout.Window` to handle this particular
        event.)
        """
        if self._fragments:
            # Read the generator.
            fragments_for_line = list(split_lines(self._fragments))

            try:
                fragments = fragments_for_line[mouse_event.position.y]
            except IndexError:
                return NotImplemented
            else:
                # Find position in the fragment list.
                xpos = mouse_event.position.x

                # Find mouse handler for this character.
                count = 0
                for item in fragments:
                    count += len(item[1])
                    if count > xpos:
                        if len(item) >= 3:
                            # Handler found. Call it.
                            # (Handler can return NotImplemented, so return
                            # that result.)
                            handler = item[2]  # type: ignore
                            return handler(mouse_event)
                        else:
                            break

        # Otherwise, don't handle here.
        return NotImplemented



class Bar:
    def __init__(self, message: Optional[str] = None):
        self.message=message


    def draw(self, align="center", fg:str="black", bg:str="aquamarine"):
        return container(Window(FormattedTextItem(self.message), height=1, style="fg:"+ fg + " bg:" + bg, align=align))
