"""
Line editing functionality.
---------------------------

This provides a UI for a line input, similar to GNU Readline, libedit and
linenoise.

Either call the :func:`prompt` function for every line input. Or create an instance
of the :class:`.Prompt` class and call the `prompt` method from that
class. In the second case, we'll have an instance that keeps all the state like
the history in between several calls.

"""
from asyncio import get_event_loop
import warnings
from contextlib import contextmanager
from enum import Enum
from functools import partial
from typing import (
    TYPE_CHECKING,
    Callable,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)


from quo.console.console import Console
from quo.console.current import get_app
from quo.completion.auto_suggest import AutoSuggest, DynamicAutoSuggest
from quo.buffer import Buffer
from quo.clipboard import Clipboard, DynamicClipboard, InMemoryClipboard
from quo.completion import Completer, DynamicCompleter, ThreadedCompleter
from quo.document import Document
from quo.enums import DEFAULT_BUFFER, SEARCH_BUFFER, EditingMode
from quo.filters import (
    Condition,
    FilterOrBool,
    has_arg,
    has_focus,
    is_done,
    is_true,
    renderer_height_is_known,
    to_filter,
)
from quo.text import (
    AnyFormattedText,
    StyleAndTextTuples,
    fragment_list_to_text,
    merge_formatted_text,
    to_formatted_text,
)
from quo.history import History, InMemoryHistory
from quo.input.core import Input
from quo.keys.key_binding.bindings.auto_suggest import load_auto_suggest_bindings
from quo.keys.key_binding.bindings.completion import (
    display_completions_like_readline,
)
from quo.keys.key_binding.bindings.open_in_editor import (
    load_open_in_editor_bindings,
)
from quo.keys import Keys, KeyBinder
from quo.keys.key_binding.key_bindings import (
    ConditionalKeyBindings,
    DynamicKeyBindings,
    KeyBindingsBase,
    merge_key_bindings,
)
from quo.keys.key_binding.key_processor import KeyPressEvent
from quo.layout.containers import Float, FloatContainer, HSplit, Window
from quo.layout.containers import ConditionalContainer, WindowAlign
from quo.layout.controls import (
    BufferControl,
    FormattedTextControl,
    SearchBufferControl,
)
from quo.layout.dimension import Dimension
from quo.layout.layout import Layout
from quo.layout.menus import CompletionsMenu, MultiColumnCompletionsMenu
from quo.layout.processors import (
    AfterInput,
    AppendAutoSuggestion,
    ConditionalProcessor,
    DisplayMultipleCursors,
    DynamicProcessor,
    HighlightIncrementalSearchProcessor,
    HighlightSelectionProcessor,
    PasswordProcessor,
    Processor,
    ReverseSearchProcessor,
    merge_processors,
)

from quo.layout.utils import explode_text_fragments
from quo.highlight import DynamicLexer, Lexer
from quo.output import ColorDepth, DummyOutput, Output
from quo.style import (
    BaseStyle,
    ConditionalStyleTransformation,
    DynamicStyle,
    DynamicStyleTransformation,
    StyleTransformation,
    SwapLightAndDarkStyleTransformation,
    merge_style_transformations,
    )

from quo.utils.utils import get_width as get_cwidth
from quo.utils.utils import (
    is_dumb_terminal,
    suspend_to_background_supported,
    to_str,
)
from quo.types import DynamicValidator, Validator
from quo.widget.toolbars import (
    SearchToolbar,
    SystemToolbar,
    ValidationToolbar,
)

if TYPE_CHECKING:
    from quo.text.core import MagicFormattedText

__all__ = [
    "prompt",
    "Prompt",
    "CompleteStyle",
]

_StyleAndTextTuplesCallable = Callable[[], StyleAndTextTuples]
E = KeyPressEvent


def _split_multiline_elicit(
    get_elicit_text: _StyleAndTextTuplesCallable,
) -> Tuple[
    Callable[[], bool], _StyleAndTextTuplesCallable, _StyleAndTextTuplesCallable
]:
    """
    Take a `get_elicit_text` function and return three new functions instead.
    One that tells whether this elicit consists of multiple lines; one that
    returns the fragments to be shown on the lines above the input; and another
    one with the fragments to be shown at the first line of the input.
    """

    def has_before_fragments() -> bool:
        for fragment, char, *_ in get_elicit_text():
            if "\n" in char:
                return True
        return False

    def before() -> StyleAndTextTuples:
        result: StyleAndTextTuples = []
        found_nl = False
        for fragment, char, *_ in reversed(explode_text_fragments(get_elicit_text())):
            if found_nl:
                result.insert(0, (fragment, char))
            elif char == "\n":
                found_nl = True
        return result

    def first_input_line() -> StyleAndTextTuples:
        result: StyleAndTextTuples = []
        for fragment, char, *_ in reversed(explode_text_fragments(get_elicit_text())):
            if char == "\n":
                break
            else:
                result.insert(0, (fragment, char))
        return result

    return has_before_fragments, before, first_input_line


class _Relicit(Window):
    """
    The prompt that is displayed on the right side of the Window.
    """

    def __init__(self, text: AnyFormattedText) -> None:
        super().__init__(
            FormattedTextControl(text=text),
            align=WindowAlign.RIGHT,
            style="class:rprompt",
        )


class CompleteStyle(str, Enum):
    """
    How to display autocompletions for the prompt.
    """

    value: str

    single_column= "single_column"
    multi_column = "multi_column"
    neat = "neat"


# Formatted text for the continuation elicit. It's the same like other
# formatted text, except that if it's a callable, it takes three arguments.
ElicitContinuationText = Union[
    str,
    "MagicFormattedText",
    StyleAndTextTuples,
    # (elicit_width, line_number, wrap_count) -> AnyFormattedText.
    Callable[[int, int, int], AnyFormattedText],
]

_T = TypeVar("_T")

##

def prompt(
    text: str,
    default: str = None,
    hide=False,
    affirm=False,
    type=None,
    value_proc=None,
    suffix: str = ":> ",
    show_default=True,
    err=False,
    show_choices=True,
):

    """Prompts a user for input.  This is a convenience function that can be used to prompt a user for input later.

    If the user aborts the input by sending a interrupt signal, this  function will catch it and raise a :exc:`Abort` exception.

    :param text: the text to show for the prompt.
    :param default: the default value to use if no input happens.  If this  is not given it will prompt until it's aborted.
    :param hide: if this is set to true then the input value will  be hidden.
    :param affirm: asks for confirmation for the value.
    :param type: the type to use to check the value against.
    :param value_proc: if this parameter is provided it's a function that is invoked instead of the type conversion to convert a value.
    :param suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of ``stdout``, the same as with echo.
    :param show_choices: Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is "Group by" then the  prompt will be "Group by (day, week): ".
    Example usage::
    s = prompt("")


    """
    from quo.types import convert_type
    from quo.expediency import inscribe
    from quo.errors import Abort, UsageError
    from quo.i_o.termui import _build_prompt, hidden_prompt_func
    insert = input
    result = None


    def prompt_func(text):
        f = hidden_prompt_func if hide else insert
        try:
            inscribe(text, nl=False, err=err)
            return f("")
        except (KeyboardInterrupt, EOFError):
            # getpass doesn't print a newline if the user aborts input with ^C.
            # Allegedly this behavior is inherited from getpass(3).
            # A doc bug has been filed at https://bugs.python.org/issue24711
            if hide:
                inscribe(None, err=err)
            raise Abort("You've aborted input")

    if value_proc is None:
        value_proc = convert_type(type, default)

    prompt = _build_prompt(
        text, suffix, show_default, default, show_choices, type
    )

    while 1:
        while 1:
            value = prompt_func(prompt)
            if value:
                break
            elif default is not None:
                value = default
                break
        try:
            result = value_proc(value)
        except UsageError as e:
            if hide:
                inscribe("ERROR: the value you entered was invalid", err=err)
            else:
                inscribe(f"Error: {e.message}", err=err)  # noqa: B306
            continue
        if not affirm:
            return result
        while 1:
            value2 = prompt_func("Repeat for confirmation: ")
            if value2:
                break
        if value == value2:
            return result
        from quo.i_o.termui import echo
        echo(f"ERROR:", nl=False, fg="black", bg="red")
        echo(f" ", nl=False)
        echo(f"The two entered values do not match", err=err, fg="black", bg="yellow")





class Prompt(Generic[_T]):
    """
    This can be used as a GNU Readline
    replacement.

    It is a wrapper around a lot of ``quo`` functionality and can
    be a replacement for `input`.

    All parameters that expect "formatted text" can take either just plain text
    (a unicode object), a list of ``(style_str, text)`` tuples or an HTML object.

    Example usage::

        s = Prompt(message='>')
        text = s.prompt()

    :param text: Plain text or formatted text to be shown before the elicit.
        This can also be a callable that returns formatted text.
    :param multiline: `bool` or :class:`~quo.filters.Filter`.
        When True, prefer a layout that is more adapted for multiline input.
        Text after newlines is automatically indented, and search/arg input is
        shown below the input, instead of replacing the elicit.
    :param wrap_lines: `bool` or :class:`~quo.filters.Filter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.
    :param hide: Show asterisks instead of the actual typed characters.
    :param editing_mode: ``EditingMode.VI`` or ``EditingMode.EMACS``.
    :param vi_mode: `bool`, if True, Identical to ``editing_mode=EditingMode.VI``.
    :param complete_while_typing: `bool` or
        :class:`~quo.filters.Filter`. Enable autocompletion while
        typing.
    :param validate_while_typing: `bool` or
        :class:`~quo.filters.Filter`. Enable input validation while
        typing.
    :param enable_history_search: `bool` or
        :class:`~quo.filters.Filter`. Enable up-arrow parting
        string matching.
    :param search_ignore_case:
        :class:`~quo.filters.Filter`. Search case insensitive.
    :param highlighter: :class:`~quo.lexers.Lexer` to be used for the
        syntax highlighting.
    :param type: :class:`~quo.types.Validator` instance
        for input validation.
    :param completer: :class:`~quo.completion.Completer` instance
        for input completion.
    :param complete_in_thread: `bool` or
        :class:`~quo.filters.Filter`. Run the completer code in a
        background thread in order to avoid blocking the user interface.
        For ``CompleteStyle.READLINE_LIKE``, this setting has no effect. There
        we always run the completions in the main thread.
    :param reserve_space_for_menu: Space to be reserved for displaying the menu.
        (0 means that no space needs to be reserved.)
    :param auto_suggest: :class:`~quo.completion.auto_suggest.AutoSuggest`
        instance for input suggestions.
    :param style: :class:`.Style` instance for the color scheme.
    :param include_default_pygments_style: `bool` or
        :class:`~quo.filters.Filter`. Tell whether the default
        styling for Pygments lexers has to be included. By default, this is
        true, but it is recommended to be disabled if another Pygments style is
        passed as the `style` argument, otherwise, two Pygments styles will be
        merged.
    :param style_transformation:
        :class:`~quo.style.StyleTransformation` instance.
    :param swap_light_and_dark_colors: `bool` or
        :class:`~quo.filters.Filter`. When enabled, apply
        :class:`~quo.style.SwapLightAndDarkStyleTransformation`.
        This is useful for switching between dark and light terminal
        backgrounds.
    :param system_prompt: `bool` or
        :class:`~quo.filters.Filter`. Pressing Meta+'!' will show
        a system elicit.
    :param enable_suspend: `bool` or :class:`~quo.filters.Filter`.
        Enable Control-Z style suspension.
    :param enable_open_in_editor: `bool` or
        :class:`~quo.filters.Filter`. Pressing 'v' in Vi mode or
        C-X C-E in emacs mode will open an external editor.
    :param history: :class:`~quo.history.History` instance.
    :param clipboard: :class:`~quo.clipboard.Clipboard` instance.
        (e.g. :class:`~quo.clipboard.InMemoryClipboard`)
    :param rprompt: Text or formatted text to be displayed on the right side.
        This can also be a callable that returns (formatted) text.
    :param bottom_toolbar: Formatted text or callable which is supposed to
        return formatted text.
    :param elicit_continuation: Text that needs to be displayed for a multiline
        elicit continuation. This can either be formatted text or a callable
        that takes a `elicit_width`, `line_number` and `wrap_count` as input
        and returns formatted text. When this is `None` (the default), then
        `elicit_width` spaces will be used.
    :param complete_style: ``CompleteStyle.COLUMN``,
        ``CompleteStyle.MULTI_COLUMN`` or ``CompleteStyle.READLINE_LIKE``.
    :param mouse_support: `bool` or :class:`~quo.filters.Filter`
        to enable mouse support.
    :param placeholder: Text to be displayed when no input has been given
        yet. Unlike the `default` parameter, this won't be returned as part of
        the output ever. This can be formatted text or a callable that returns
        formatted text.
    :param refresh_interval: (number; in seconds) When given, refresh the UI
        every so many seconds.
    :param input: `Input` object. (Note that the preferred way to change the
        input/output is by creating an `AppSession`.)
    :param output: `Output` object.
    """

    _fields = (
        "text",
        "highlighter",
        "completer",
        "complete_in_thread",
        "is_password",
        "editing_mode",
        "bind",
        "is_password",
        "hide",
        "bottom_toolbar",
        "style",
        "style_transformation",
        "swap_light_and_dark_colors",
        "color_depth",
        "include_default_pygments_style",
        "rprompt",
        "multiline",
        "prompt_continuation",
        "wrap_lines",
        "enable_history_search",
        "search_ignore_case",
        "dynamic_completion",
        "complete_while_typing",
        "validate_while_typing",
        "complete_style",
        "mouse_support",
        "auto_suggest",
        "clipboard",
        "type",
        "refresh_interval",
        "input_processors",
        "placeholder",
        "enable_system_elicit",
        "enable_suspend",
        "enable_open_in_editor",
        "reserve_space_for_menu",
        "tempfile_suffix",
        "tempfile",
    )

    def __init__(
        self,
        text: AnyFormattedText = "",
        *,
        multiline: FilterOrBool = False,
        wrap_lines: FilterOrBool = True,
        is_password: FilterOrBool = False,
        hide: FilterOrBool = False,
        vi_mode: bool = False,
        editing_mode: EditingMode = EditingMode.EMACS,
        complete_while_typing: FilterOrBool = True,
        validate_while_typing: FilterOrBool = True,
        enable_history_search: FilterOrBool = True, #False,
        search_ignore_case: FilterOrBool = False,
        highlighter: Optional[Lexer] = None,
        system_prompt: FilterOrBool = False,
        suspend: FilterOrBool = False,
        enable_open_in_editor: FilterOrBool = False,
        type: Optional[Validator] = None,
        completer: Optional[Completer] = None,
        complete_in_thread: bool = False,
        reserve_space_for_menu: int = 8,
        complete_style: CompleteStyle = CompleteStyle.single_column,
        auto_suggest: Optional[AutoSuggest] = None,
        style: Optional[BaseStyle] = None,
        style_transformation: Optional[StyleTransformation] = None,
        swap_light_and_dark_colors: FilterOrBool = False,
        color_depth: Optional[ColorDepth] = None,
        include_default_pygments_style: FilterOrBool = True,
        history: Optional[History] = None,
        clipboard: Optional[Clipboard] = None,
        prompt_continuation: Optional[ElicitContinuationText] = None,
        rprompt: AnyFormattedText = None,
        bottom_toolbar: AnyFormattedText = None,
        mouse_support: FilterOrBool = False,
        input_processors: Optional[List[Processor]] = None,
        placeholder: Optional[AnyFormattedText] = None,
        bind: Optional[KeyBindingsBase] = None,
        erase_when_done: bool = False,
        tempfile_suffix: Optional[Union[str, Callable[[], str]]] = ".txt",
        tempfile: Optional[Union[str, Callable[[], str]]] = None,
        refresh_interval: float = 0,
        input: Optional[Input] = None,
        output: Optional[Output] = None,
    ) -> None:

        history = history or InMemoryHistory()
        clipboard = clipboard or InMemoryClipboard()

        # Ensure backwards-compatibility, when `vi_mode` is passed.
        if vi_mode:
            editing_mode = EditingMode.VI

        # Store all settings in this class.
        self._input = input
        self._output = output

        # Store attributes.
        # (All except 'editing_mode'.)
        self.text = text
        self.highlighter = highlighter
        self.completer = completer
        self.complete_in_thread = complete_in_thread
        self.is_password =is_password or hide
        self.bind= bind
        self.bottom_toolbar = bottom_toolbar
        self.style = style
        self.style_transformation = style_transformation
        self.swap_light_and_dark_colors = swap_light_and_dark_colors
        self.color_depth = color_depth
        self.include_default_pygments_style = include_default_pygments_style
        self.rprompt = rprompt
        self.multiline = multiline
        self.prompt_continuation = prompt_continuation
        self.wrap_lines = wrap_lines
        self.enable_history_search = enable_history_search
        self.search_ignore_case = search_ignore_case
        self.complete_while_typing = complete_while_typing
        self.validate_while_typing = validate_while_typing
        self.complete_style = complete_style
        self.mouse_support = mouse_support
        self.auto_suggest = auto_suggest
        self.clipboard = clipboard
        self.type = type
        self.refresh_interval = refresh_interval
        self.input_processors = input_processors
        self.placeholder = placeholder
        self.system_prompt = system_prompt
        self.suspend = suspend
        self.enable_open_in_editor = enable_open_in_editor
        self.reserve_space_for_menu = reserve_space_for_menu
        self.tempfile_suffix = tempfile_suffix
        self.tempfile = tempfile

        # Create buffers, layout and Application.
        self.history = history
        self.default_buffer = self._create_default_buffer()
        self.search_buffer = self._create_search_buffer()
        self.layout = self._create_layout()
        self.app = self._create_application(editing_mode, erase_when_done)

    def _dyncond(self, attr_name: str) -> Condition:
        """
        Dynamically take this setting from this 'Prompt' class.
        `attr_name` represents an attribute name of this class. Its value
        can either be a boolean or a `Filter`.

        This returns something that can be used as either a `Filter`
        or `Filter`.
        """

        @Condition
        def dynamic() -> bool:
            value = cast(FilterOrBool, getattr(self, attr_name))
            return to_filter(value)()

        return dynamic

    def _create_default_buffer(self) -> Buffer:
        """
        Create and return the default input buffer.
        """
        dyncond = self._dyncond

        # Create buffers list.
        def accept(buff: Buffer) -> bool:
            """Accept the content of the default buffer. This is called when
            the validation succeeds."""
            cast(Console[str], get_app()).exit(result=buff.document.text)
            return True  # Keep text, we call 'reset' later on.

        return Buffer(
            name=DEFAULT_BUFFER,
            # Make sure that complete_while_typing is disabled when
            # enable_history_search is enabled. (First convert to Filter,
            # to avoid doing bitwise operations on bool objects.)
            complete_while_typing=Condition(
                lambda: is_true(self.complete_while_typing)
                and not is_true(self.enable_history_search)
                and not self.complete_style == CompleteStyle.neat
            ),
            validate_while_typing=dyncond("validate_while_typing"),
            enable_history_search=dyncond("enable_history_search"),
            type=DynamicValidator(lambda: self.type),
            completer=DynamicCompleter(
                lambda: ThreadedCompleter(self.completer)
                if self.complete_in_thread and self.completer
                else self.completer
            ),
            history=self.history,
            auto_suggest=DynamicAutoSuggest(lambda: self.auto_suggest),
            accept_handler=accept,
            tempfile_suffix=lambda: to_str(self.tempfile_suffix or ""),
            tempfile=lambda: to_str(self.tempfile or ""),
        )

    def _create_search_buffer(self) -> Buffer:
        return Buffer(name=SEARCH_BUFFER)

    def _create_layout(self) -> Layout:
        """
        Create `Layout` for this prompt.
        """
        dyncond = self._dyncond

        # Create functions that will dynamically split the elicit. (If we have
        # a multiline elicit.)
        (
            has_before_fragments,
            get_elicit_text_1,
            get_elicit_text_2,
        ) = _split_multiline_elicit(self._get_elicit)

        default_buffer = self.default_buffer
        search_buffer = self.search_buffer

        # Create processors list.
        @Condition
        def display_placeholder() -> bool:
            return self.placeholder is not None and self.default_buffer.text == ""

        all_input_processors = [
            HighlightIncrementalSearchProcessor(),
            HighlightSelectionProcessor(),
            ConditionalProcessor(
                AppendAutoSuggestion(), has_focus(default_buffer) & ~is_done
            ),
            ConditionalProcessor(PasswordProcessor(), dyncond("is_password")),
            DisplayMultipleCursors(),
            # Users can insert processors here.
            DynamicProcessor(lambda: merge_processors(self.input_processors or [])),
            ConditionalProcessor(
                AfterInput(lambda: self.placeholder),
                filter=display_placeholder,
            ),
        ]

        # Create bottom toolbars.
        bottom_toolbar = ConditionalContainer(
            Window(
                FormattedTextControl(
                    lambda: self.bottom_toolbar, style="class:bottom-toolbar.text"
                ),
                style="class:bottom-toolbar",
                dont_extend_height=True,
                height=Dimension(min=1),
            ),
            filter=~is_done
            & renderer_height_is_known
            & Condition(lambda: self.bottom_toolbar is not None),
        )

        search_toolbar = SearchToolbar(
            search_buffer, ignore_case=dyncond("search_ignore_case")
        )

        search_buffer_control = SearchBufferControl(
            buffer=search_buffer,
            input_processors=[ReverseSearchProcessor()],
            ignore_case=dyncond("search_ignore_case"),
        )

        system_toolbar = SystemToolbar(
            enable_global_bindings=dyncond("system_prompt")
        )

        def get_search_buffer_control() -> SearchBufferControl:
            "Return the UIControl to be focused when searching start."
            if is_true(self.multiline):
                return search_toolbar.control
            else:
                return search_buffer_control

        default_buffer_control = BufferControl(
            buffer=default_buffer,
            search_buffer_control=get_search_buffer_control,
            input_processors=all_input_processors,
            include_default_input_processors=False,
            highlighter=DynamicLexer(lambda: self.highlighter),
            preview_search=True,
        )

        default_buffer_window = Window(
            default_buffer_control,
            height=self._get_default_buffer_control_height,
            get_line_prefix=partial(
                self._get_line_prefix, get_elicit_text_2=get_elicit_text_2
            ),
            wrap_lines=dyncond("wrap_lines"),
        )

        @Condition
        def multi_column_complete_style() -> bool:
            return self.complete_style == CompleteStyle.multi_column

        # Build the layout.
        layout = HSplit(
            [
                # The main input, with completion menus floating on top of it.
                FloatContainer(
                    HSplit(
                        [
                            ConditionalContainer(
                                Window(
                                    FormattedTextControl(get_elicit_text_1),
                                    dont_extend_height=True,
                                ),
                                Condition(has_before_fragments),
                            ),
                            ConditionalContainer(
                                default_buffer_window,
                                Condition(
                                    lambda: get_app().layout.current_control
                                    != search_buffer_control
                                ),
                            ),
                            ConditionalContainer(
                                Window(search_buffer_control),
                                Condition(
                                    lambda: get_app().layout.current_control
                                    == search_buffer_control
                                ),
                            ),
                        ]
                    ),
                    [
                        # Completion menus.
                        # NOTE: Especially the multi-column menu needs to be
                        #       transparent, because the shape is not always
                        #       rectangular due to the meta-text below the menu.
                        Float(
                            xcursor=True,
                            ycursor=True,
                            transparent=True,
                            content=CompletionsMenu(
                                max_height=16,
                                scroll_offset=1,
                                extra_filter=has_focus(default_buffer)
                                & ~multi_column_complete_style,
                            ),
                        ),
                        Float(
                            xcursor=True,
                            ycursor=True,
                            transparent=True,
                            content=MultiColumnCompletionsMenu(
                                show_meta=True,
                                extra_filter=has_focus(default_buffer)
                                & multi_column_complete_style,
                            ),
                        ),
                        # The right elicit.
                        Float(
                            right=0,
                            bottom=0,
                            hide_when_covering_content=True,
                            content=_Relicit(lambda: self.rprompt),
                        ),
                    ],
                ),
                ConditionalContainer(ValidationToolbar(), filter=~is_done),
                ConditionalContainer(
                    system_toolbar, dyncond("system_prompt") & ~is_done
                ),
                # In multiline mode, we use two toolbars for 'arg' and 'search'.
                ConditionalContainer(
                    Window(FormattedTextControl(self._get_arg_text), height=1),
                    dyncond("multiline") & has_arg,
                ),
                ConditionalContainer(search_toolbar, dyncond("multiline") & ~is_done),
                bottom_toolbar,
            ]
        )

        return Layout(layout, default_buffer_window)

    def _create_application(
        self, editing_mode: EditingMode, erase_when_done: bool
    ) -> Console[_T]:
        """
        Create the `Console` object.
        """
        dyncond = self._dyncond

        # Default key bindings.
        auto_suggest_bindings = load_auto_suggest_bindings()
        open_in_editor_bindings = load_open_in_editor_bindings()
        elicit_bindings = self._create_elicit_bindings()

        # Create console application
        application: Console[_T] = Console(
            layout=self.layout,
            style=DynamicStyle(lambda: self.style),
            style_transformation=merge_style_transformations(
                [
                    DynamicStyleTransformation(lambda: self.style_transformation),
                    ConditionalStyleTransformation(
                        SwapLightAndDarkStyleTransformation(),
                        dyncond("swap_light_and_dark_colors"),
                    ),
                ]
            ),
            include_default_pygments_style=dyncond("include_default_pygments_style"),
            clipboard=DynamicClipboard(lambda: self.clipboard),
            bind=merge_key_bindings(
                [
                    merge_key_bindings(
                        [
                            auto_suggest_bindings,
                            ConditionalKeyBindings(
                                open_in_editor_bindings,
                                dyncond("enable_open_in_editor")
                                & has_focus(DEFAULT_BUFFER),
                            ),
                            elicit_bindings,
                        ]
                    ),
                    DynamicKeyBindings(lambda: self.bind),
                ]
            ),
            mouse_support=dyncond("mouse_support"),
            editing_mode=editing_mode,
            erase_when_done=erase_when_done,
            reverse_vi_search_direction=True,
            color_depth=lambda: self.color_depth,
            refresh_interval=self.refresh_interval,
            input=self._input,
            output=self._output,
        )

        # During render time, make sure that we focus the right search control
        # (if we are searching). - This could be useful if people make the
        # 'multiline' property dynamic.
        """
        def on_render(app):
            multiline = is_true(self.multiline)
            current_control = app.layout.current_control

            if multiline:
                if current_control == search_buffer_control:
                    app.layout.current_control = search_toolbar.control
                    app.invalidate()
            else:
                if current_control == search_toolbar.control:
                    app.layout.current_control = search_buffer_control
                    app.invalidate()

        app.on_render += on_render
        """

        return application

    def _create_elicit_bindings(self) -> KeyBinder:
        """
        Create the KeyBindings for a prompt application.
        """
        kb = KeyBinder()
        handle = kb.add
        default_focused = has_focus(DEFAULT_BUFFER)

        @Condition
        def do_accept() -> bool:
            return not is_true(self.multiline) and self.app.layout.has_focus(
                DEFAULT_BUFFER
            )

        @handle("enter", filter=do_accept & default_focused)
        def _accept_input(event: E) -> None:
            "Accept input when enter has been pressed."
            self.default_buffer.validate_and_handle()

        @Condition
        def readline_complete_style() -> bool:
            return self.complete_style == CompleteStyle.neat

        @handle("tab", filter=readline_complete_style & default_focused)
        def _complete_like_readline(event: E) -> None:
            "Display completions (like Readline)."
            display_completions_like_readline(event)

        @handle("ctrl-c", filter=default_focused)
        def _keyboard_interrupt(event: E) -> None:
            "Abort when Control-C has been pressed."
            event.app.exit(exception=KeyboardInterrupt, style="class:aborting")

        @Condition
        def ctrl_d_condition() -> bool:
            """Ctrl-D binding is only active when the default buffer is selected
            and empty."""
            app = get_app()
            return (
                app.current_buffer.name == DEFAULT_BUFFER
                and not app.current_buffer.text
            )

        @handle("ctrl-d", filter=ctrl_d_condition & default_focused)
        def _eof(event: E) -> None:
            "Exit when Control-D has been pressed."
            event.app.exit(exception=EOFError, style="class:exiting")

        suspend_supported = Condition(suspend_to_background_supported)

        @Condition
        def enable_suspend() -> bool:
            return to_filter(self.suspend)()

        @handle("ctrl-z", filter=suspend_supported & enable_suspend)
        def _suspend(event: E) -> None:
            """
            Suspend process to background.
            """
            event.app.suspend_to_background()

        return kb

    def prompt(
        self,
        text: Optional[AnyFormattedText] = None,
        *,
        editing_mode: Optional[EditingMode] = None,
        refresh_interval: Optional[float] = None,
        vi_mode: Optional[bool] = None,
        highlighter: Optional[Lexer] = None,
        completer: Optional[Completer] = None,
        complete_in_thread: Optional[bool] = None,
        is_password: Optional[bool] = None,
        hide: Optional[bool] = False,
        bind: Optional[KeyBindingsBase] = None,
        bottom_toolbar: Optional[AnyFormattedText] = None,
        style: Optional[BaseStyle] = None,
        color_depth: Optional[ColorDepth] = None,
        default_pygments_style: Optional[FilterOrBool] = None,
        style_transformation: Optional[StyleTransformation] = None,
        swap_light_and_dark_colors: Optional[FilterOrBool] = None,
        rprompt: Optional[AnyFormattedText] = None,
        multiline: Optional[FilterOrBool] = None,
        elicit_continuation: Optional[ElicitContinuationText] = None,
        wrap_lines: Optional[FilterOrBool] = None,
        enable_history_search: Optional[FilterOrBool] = None,
        search_ignore_case: Optional[FilterOrBool] = None,
        complete_while_typing: Optional[FilterOrBool] = None,
        validate_while_typing: Optional[FilterOrBool] = None,
        complete_style: Optional[CompleteStyle] = None,
        auto_suggest: Optional[AutoSuggest] = None,
        type: Optional[Validator] = None,
        clipboard: Optional[Clipboard] = None,
        mouse_support: Optional[FilterOrBool] = None,
        input_processors: Optional[List[Processor]] = None,
        placeholder: Optional[AnyFormattedText] = None,
        reserve_space_for_menu: Optional[int] = None,
        system_prompt: Optional[FilterOrBool] = None,
        suspend: Optional[FilterOrBool] = None,
        enable_open_in_editor: Optional[FilterOrBool] = None,
        tempfile_suffix: Optional[Union[str, Callable[[], str]]] = None,
        tempfile: Optional[Union[str, Callable[[], str]]] = None,
        # Following arguments are specific to the current `elicit()` call.
        default: Union[str, Document] = "",
        accept_default: bool = False,
        pre_run: Optional[Callable[[], None]] = None,
        set_exception_handler: bool = True,
        in_thread: bool = False,
    ) -> _T:
        """
        Display the prompt.

        The first set of arguments is a subset of the :class:`~.Prompt`
        class itself. For these, passing in ``None`` will keep the current
        values that are active in the session. Passing in a value will set the
        attribute for the session, which means that it applies to the current,
        but also to the next Prompt.

        Note that in order to erase a ``Completer``, ``Validator`` or
        ``AutoSuggest``, you can't use ``None``. Instead pass in a
        ``DummyCompleter``, ``DummyValidator`` or ``DummyAutoSuggest`` instance
        respectively. For a ``Lexer`` you can pass in an empty ``SimpleLexer``.

        Additional arguments, specific for this elicit:

        :param default: The default input text to be shown. (This can be edited
            by the user).
        :param accept_default: When `True`, automatically accept the default
            value without allowing the user to edit the input.
        :param pre_run: Callable, called at the start of `Application.run`.
        :param in_thread: Run the elicit in a background thread; block the
            current thread. This avoids interference with an event loop in the
            current thread. Like `Application.run(in_thread=True)`.

        This method will raise ``KeyboardInterrupt`` when control-c has been
        pressed (for abort) and ``EOFError`` when control-d has been pressed
        (for exit).
        """
        # NOTE: We used to create a backup of the Prompt attributes and
        #       restore them after exiting the elicit. This code has been
        #       removed, because it was confusing and didn't really serve a use
        #       case. (People were changing `Application.editing_mode`
        #       dynamically and surprised that it was reset after every call.)

        # NOTE 2: YES, this is a lot of repeation below...
        #         However, it is a very convenient for a user to accept all
        #         these parameters in this `prompt` method as well. We could
        #         use `locals()` and `setattr` to avoid the repetition, but
        #         then we loose the advantage of mypy and pyflakes to be able
        #         to verify the code.
        if text is not None:
            self.text = text
        if editing_mode is not None:
            self.editing_mode = editing_mode
        if refresh_interval is not None:
            self.refresh_interval = refresh_interval
        if vi_mode:
            self.editing_mode = EditingMode.VI
        if highlighter is not None:
            self.highlighter = highlighter
        if completer is not None:
            self.completer = completer
        if complete_in_thread is not None:
            self.complete_in_thread = complete_in_thread
        if is_password is not None:
            self.is_password = is_password or hide
        if hide is not None:
            self.hide = hide or is_password
        if bind is not None:
            self.bind = bind
        if bottom_toolbar is not None:
            self.bottom_toolbar = bottom_toolbar
        if style is not None:
            self.style = style
        if color_depth is not None:
            self.color_depth = color_depth
        if default_pygments_style is not None:
            self.default_pygments_style = default_pygments_style
        if style_transformation is not None:
            self.style_transformation = style_transformation
        if swap_light_and_dark_colors is not None:
            self.swap_light_and_dark_colors = swap_light_and_dark_colors
        if rprompt is not None:
            self.rprompt = rprompt
        if multiline is not None:
            self.multiline = multiline
        if elicit_continuation is not None:
            self.elicit_continuation = elicit_continuation
        if wrap_lines is not None:
            self.wrap_lines = wrap_lines
        if enable_history_search is not None:
            self.enable_history_search = enable_history_search
        if search_ignore_case is not None:
            self.search_ignore_case = search_ignore_case
        if complete_while_typing is not None:
            self.complete_while_typing = complete_while_typing
        if validate_while_typing is not None:
            self.validate_while_typing = validate_while_typing
        if complete_style is not None:
            self.complete_style = complete_style
        if auto_suggest is not None:
            self.auto_suggest = auto_suggest
        if type is not None:
            self.type = type
        if clipboard is not None:
            self.clipboard = clipboard
        if mouse_support is not None:
            self.mouse_support = mouse_support
        if input_processors is not None:
            self.input_processors = input_processors
        if placeholder is not None:
            self.placeholder = placeholder
        if reserve_space_for_menu is not None:
            self.reserve_space_for_menu = reserve_space_for_menu
        if system_prompt is not None:
            self.system_prompt = system_prompt
        if suspend is not None:
            self.suspend = suspend
        if enable_open_in_editor is not None:
            self.enable_open_in_editor = enable_open_in_editor
        if tempfile_suffix is not None:
            self.tempfile_suffix = tempfile_suffix
        if tempfile is not None:
            self.tempfile = tempfile

        self._add_pre_run_callables(pre_run, accept_default)
        self.default_buffer.reset(
            default if isinstance(default, Document) else Document(default)
        )
        self.app.refresh_interval = self.refresh_interval  # This is not reactive.

        # If we are using the default output, and have a dumb terminal. Use the
        # dumb elicit.
        if self._output is None and is_dumb_terminal():
            with self._dumb_elicit(self.message) as dump_app:
                return dump_app.run(in_thread=in_thread)

        return self.app.run(
            set_exception_handler=set_exception_handler, in_thread=in_thread
        )

    @contextmanager
    def _dumb_elicit(self, message: AnyFormattedText = "") -> Iterator[Console[_T]]:
        """
        Create prompt `Console` for prompt function for dumb terminals.

        Dumb terminals have minimum rendering capabilities. We can only print
        text to the screen. We can't use colors, and we can't do cursor
        movements. The Emacs inferior shell is an example of a dumb terminal.

        We will show the elicit, and wait for the input. We still handle arrow
        keys, and all custom key bindings, but we don't really render the
        cursor movements. Instead we only print the typed character that's
        right before the cursor.
        """
        # Send prompt to output.
        self.output.write(fragment_list_to_text(to_formatted_text(self.text)))
        self.output.flush()

        # Key bindings for the dumb elicit: mostly the same as the full elicit(prompt)
        bind: KeyBindingsBase = self._create_elicit_bindings()
        if self.bind:
            bind = merge_key_bindings([self.bind, bind])

        # Create and run application.
        application = cast(
            Console[_T],
            Console(
                input=self.input,
                output=DummyOutput(),
                layout=self.layout,
                bind=bind,
            ),
        )

        def on_text_changed(_: object) -> None:
            self.output.write(self.default_buffer.document.text_before_cursor[-1:])
            self.output.flush()

        self.default_buffer.on_text_changed += on_text_changed

        try:
            yield application
        finally:
            # Render line ending.
            self.output.write("\r\n")
            self.output.flush()

            self.default_buffer.on_text_changed -= on_text_changed

    async def elicit_async(
        self,
        # When any of these arguments are passed, this value is overwritten
        # in this Prompt.
        text: Optional[AnyFormattedText] = None,
        # `message` should go first, because people call it as
        # positional argument.
        *,
        editing_mode: Optional[EditingMode] = None,
        refresh_interval: Optional[float] = None,
        vi_mode: Optional[bool] = None,
        highlighter: Optional[Lexer] = None,
        completer: Optional[Completer] = None,
        complete_in_thread: Optional[bool] = None,
        is_password: Optional[bool] = None,
        hide: Optional[bool] = None,
        bind: Optional[KeyBindingsBase] = None,
        bottom_toolbar: Optional[AnyFormattedText] = None,
        style: Optional[BaseStyle] = None,
        color_depth: Optional[ColorDepth] = None,
        default_pygments_style: Optional[FilterOrBool] = None,
        style_transformation: Optional[StyleTransformation] = None,
        swap_light_and_dark_colors: Optional[FilterOrBool] = None,
        rprompt: Optional[AnyFormattedText] = None,
        multiline: Optional[FilterOrBool] = None,
        elicit_continuation: Optional[ElicitContinuationText] = None,
        wrap_lines: Optional[FilterOrBool] = None,
        enable_history_search: Optional[FilterOrBool] = None,
        search_ignore_case: Optional[FilterOrBool] = None,
        complete_while_typing: Optional[FilterOrBool] = None,
        validate_while_typing: Optional[FilterOrBool] = None,
        complete_style: Optional[CompleteStyle] = None,
        auto_suggest: Optional[AutoSuggest] = None,
        type: Optional[Validator] = None,
        clipboard: Optional[Clipboard] = None,
        mouse_support: Optional[FilterOrBool] = None,
        input_processors: Optional[List[Processor]] = None,
        placeholder: Optional[AnyFormattedText] = None,
        reserve_space_for_menu: Optional[int] = None,
        system_prompt: Optional[FilterOrBool] = None,
        suspend: Optional[FilterOrBool] = None,
        enable_open_in_editor: Optional[FilterOrBool] = None,
        tempfile_suffix: Optional[Union[str, Callable[[], str]]] = None,
        tempfile: Optional[Union[str, Callable[[], str]]] = None,
        # Following arguments are specific to the current `elicit()` call.
        default: Union[str, Document] = "",
        accept_default: bool = False,
        pre_run: Optional[Callable[[], None]] = None,
        set_exception_handler: bool = True,
    ) -> _T:

        if text is not None:
            self.text = text
        if editing_mode is not None:
            self.editing_mode = editing_mode
        if refresh_interval is not None:
            self.refresh_interval = refresh_interval
        if vi_mode:
            self.editing_mode = EditingMode.VI
        if highlighter is not None:
            self.highlighter = highlighter
        if completer is not None:
            self.completer = completer
        if complete_in_thread is not None:
            self.complete_in_thread = complete_in_thread
        if is_password is not None:
            self.is_password = is_password or hide
        if bind is not None:
            self.bind = bind
        if bottom_toolbar is not None:
            self.bottom_toolbar = bottom_toolbar
        if style is not None:
            self.style = style
        if color_depth is not None:
            self.color_depth = color_depth
        if default_pygments_style is not None:
            self.default_pygments_style = default_pygments_style
        if style_transformation is not None:
            self.style_transformation = style_transformation
        if swap_light_and_dark_colors is not None:
            self.swap_light_and_dark_colors = swap_light_and_dark_colors
        if rprompt is not None:
            self.rprompt = rprompt
        if multiline is not None:
            self.multiline = multiline
        if elicit_continuation is not None:
            self.elicit_continuation = elicit_continuation
        if wrap_lines is not None:
            self.wrap_lines = wrap_lines
        if enable_history_search is not None:
            self.enable_history_search = enable_history_search
        if search_ignore_case is not None:
            self.search_ignore_case = search_ignore_case
        if complete_while_typing is not None:
            self.complete_while_typing = complete_while_typing
        if validate_while_typing is not None:
            self.validate_while_typing = validate_while_typing
        if complete_style is not None:
            self.complete_style = complete_style
        if auto_suggest is not None:
            self.auto_suggest = auto_suggest
        if type is not None:
            self.type = type
        if clipboard is not None:
            self.clipboard = clipboard
        if mouse_support is not None:
            self.mouse_support = mouse_support
        if input_processors is not None:
            self.input_processors = input_processors
        if placeholder is not None:
            self.placeholder = placeholder
        if reserve_space_for_menu is not None:
            self.reserve_space_for_menu = reserve_space_for_menu
        if system_prompt is not None:
            self.system_prompt = system_prompt
        if suspend is not None:
            self.suspend = suspend
        if enable_open_in_editor is not None:
            self.enable_open_in_editor = enable_open_in_editor
        if tempfile_suffix is not None:
            self.tempfile_suffix = tempfile_suffix
        if tempfile is not None:
            self.tempfile = tempfile

        self._add_pre_run_callables(pre_run, accept_default)
        self.default_buffer.reset(
            default if isinstance(default, Document) else Document(default)
        )
        self.app.refresh_interval = self.refresh_interval  # This is not reactive.

        # If we are using the default output, and have a dumb terminal. Use the
        # dumb elicit.
        if self._output is None and is_dumb_terminal():
            with self._dumb_elicit(self.message) as dump_app:
                return await dump_app.run_async()

        return await self.app.run_async(set_exception_handler=set_exception_handler)

    def _add_pre_run_callables(
        self, pre_run: Optional[Callable[[], None]], accept_default: bool
    ) -> None:
        def pre_run2() -> None:
            if pre_run:
                pre_run()

            if accept_default:
                # Validate and handle input. We use `call_from_executor` in
                # order to run it "soon" (during the next iteration of the
                # event loop), instead of right now. Otherwise, it won't
                # display the default value.
                get_event_loop().call_soon(self.default_buffer.validate_and_handle)

        self.app.pre_run_callables.append(pre_run2)

    @property
    def editing_mode(self) -> EditingMode:
        return self.app.editing_mode

    @editing_mode.setter
    def editing_mode(self, value: EditingMode) -> None:
        self.app.editing_mode = value

    def _get_default_buffer_control_height(self) -> Dimension:
        # If there is an autocompletion menu to be shown, make sure that our
        # layout has at least a minimal height in order to display it.
        if (
            self.completer is not None
            and self.complete_style != CompleteStyle.neat
        ):
            space = self.reserve_space_for_menu
        else:
            space = 0

        if space and not get_app().is_done:
            buff = self.default_buffer

            # Reserve the space, either when there are completions, or when
            # `complete_while_typing` is true and we expect completions very
            # soon.
            if buff.complete_while_typing() or buff.complete_state is not None:
                return Dimension(min=space)

        return Dimension()

    def _get_elicit(self) -> StyleAndTextTuples:
        return to_formatted_text(self.text, style="class:elicit")

    def _get_continuation(
        self, width: int, line_number: int, wrap_count: int
    ) -> StyleAndTextTuples:
        """
        Insert the elicit continuation.

        :param width: The width that was used for the elicit. (more or less can  be used.)
        :param line_number:
        :param wrap_count: Amount of times that the line has been wrapped.
        """
        prompt_continuation = self.prompt_continuation

        if callable(prompt_continuation):
            continuation: AnyFormattedText = prompt_continuation(
                width, line_number, wrap_count
            )
        else:
            continuation = prompt_continuation

        # When the continuation promt is not given, choose the same width as
        # the actual elicit.
        if continuation is None and is_true(self.multiline):
            continuation = " " * width

        return to_formatted_text(continuation, style="class:elicit-continuation")

    def _get_line_prefix(
        self,
        line_number: int,
        wrap_count: int,
        get_elicit_text_2: _StyleAndTextTuplesCallable,
    ) -> StyleAndTextTuples:
        """
        Return whatever needs to be inserted before every line.
        (the elicit, or a line continuation.)
        """
        # First line: display the "arg" or the elicit.
        if line_number == 0 and wrap_count == 0:
            if not is_true(self.multiline) and get_app().key_processor.arg is not None:
                return self._inline_arg()
            else:
                return get_elicit_text_2()

        # For the next lines, display the appropriate continuation.
        elicit_width = get_cwidth(fragment_list_to_text(get_elicit_text_2()))
        return self._get_continuation(elicit_width, line_number, wrap_count)

    def _get_arg_text(self) -> StyleAndTextTuples:
        "'arg' toolbar, for in multiline mode."
        arg = self.app.key_processor.arg
        if arg is None:
            # Should not happen because of the `has_arg` filter in the layout.
            return []

        if arg == "-":
            arg = "-1"

        return [("class:arg-toolbar", "Repeat: "), ("class:arg-toolbar.text", arg)]

    def _inline_arg(self) -> StyleAndTextTuples:
        "'arg' prefix, for in single line mode."
        app = get_app()
        if app.key_processor.arg is None:
            return []
        else:
            arg = app.key_processor.arg

            return [
                ("class:elicit.arg", "(arg: "),
                ("class:elicit.arg.text", str(arg)),
                ("class:elicit.arg", ") "),
            ]

    # Expose the Input and Output objects as attributes, mainly for
    # backward-compatibility.

    @property
    def input(self) -> Input:
        return self.app.input

    @property
    def output(self) -> Output:
        return self.app.output



def create_confirm_session(
        text: str,
        suffix: str = " (y/n) "
        ) -> Prompt[bool]:
    """
    Create a `Prompt` object for the 'confirm' function.
    """
    bindings = KeyBinder()

    @bindings.add("y")
    @bindings.add("Y")
    def yes(event: E) -> None:
        session.default_buffer.text = "y"
        event.app.exit(result=True)

    @bindings.add("n")
    @bindings.add("N")
    def no(event: E) -> None:
        session.default_buffer.text = "n"
        event.app.exit(result=False)

    @bindings.add(Keys.Any)
    def _(event: E) -> None:
        "Disallow inserting other text."
        pass

    complete_message = merge_formatted_text([text, suffix])
    session: Prompt[bool] = Prompt(
        complete_message, bind=bindings
    )
    return session

def continuation(width, line_number, wrap_count):
    return '.' * width
