from contextlib import contextmanager
from quo.accordance import term_len
from quo.parser import split_opt
from quo.ui.termui import terminalsize

# Can force a width.  This is used by the test system
FORCED_WIDTH = None


def measure_table(rows):
    widths = {}
    for row in rows:
        for idx, col in enumerate(row):
            widths[idx] = max(widths.get(idx, 0), term_len(col))
    return tuple(y for x, y in sorted(widths.items()))


def iter_rows(rows, col_count):
    for row in rows:
        row = tuple(row)
        yield row + ("",) * (col_count - len(row))


def wraptext(
    text, width=78, initial_indent="", subsequent_indent="", preserve_paragraphs=False
):
    """A helper function that intelligently wraps text.  By default, it
    assumes that it operates on a single paragraph of text but if the
    `preserve_paragraphs` parameter is provided it will intelligently
    handle paragraphs (defined by two empty lines).

    If paragraphs are handled, a paragraph can be prefixed with an empty
    line containing the ``\\b`` character (``\\x08``) to indicate that
    no rewrapping should happen in that block.

    :param text: the text that should be rewrapped.
    :param width: the maximum width for the text.
    :param initial_indent: the initial indent that should be placed on the
                           first line as a string.
    :param subsequent_indent: the indent string that should be placed on
                              each consecutive line.
    :param preserve_paragraphs: if this flag is set then the wrapping will
                                intelligently handle paragraphs.
    """
    from quo.wrapper.textshawl import TextWrapper

    text = text.expandtabs()
    wrapper = TextWrapper(
        width,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        replace_whitespace=False,
    )
    if not preserve_paragraphs:
        return wrapper.fill(text)

    p = []
    buf = []
    indent = None

    def _flush_par():
        if not buf:
            return
        if buf[0].strip() == "\b":
            p.append((indent or 0, True, "\n".join(buf[1:])))
        else:
            p.append((indent or 0, False, " ".join(buf)))
        del buf[:]

    for line in text.splitlines():
        if not line:
            _flush_par()
            indent = None
        else:
            if indent is None:
                orig_len = term_len(line)
                line = line.lstrip()
                indent = orig_len - term_len(line)
            buf.append(line)
    _flush_par()

    rv = []
    for indent, raw, text in p:
        with wrapper.extra_indent(" " * indent):
            if raw:
                rv.append(wrapper.indent_only(text))
            else:
                rv.append(wrapper.fill(text))

    return "\n\n".join(rv)

#################################

"""
Wrapper for the layout.
"""
from typing import Dict, Generator, Iterable, List, Optional, Union

from quo.buffer import Buffer

from .containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    Window,
    to_container,
)
from .controls import BufferControl, SearchBufferControl, UIControl

__all__ = [
    "Layout",
    "InvalidLayoutError",
    "walk",
]

FocusableElement = Union[str, Buffer, UIControl, AnyContainer]


class Layout:
    """
    The layout for a prompt_toolkit
    :class:`~prompt_toolkit.application.Application`.
    This also keeps track of which user control is focused.

    :param container: The "root" container for the layout.
    :param focused_element: element to be focused initially. (Can be anything
        the `focus` function accepts.)
    """

    def __init__(
        self,
        container: AnyContainer,
        focused_element: Optional[FocusableElement] = None,
    ) -> None:

        self.container = to_container(container)
        self._stack: List[Window] = []

        # Map search BufferControl back to the original BufferControl.
        # This is used to keep track of when exactly we are searching, and for
        # applying the search.
        # When a link exists in this dictionary, that means the search is
        # currently active.
        # Map: search_buffer_control -> original buffer control.
        self.search_links: Dict[SearchBufferControl, BufferControl] = {}

        # Mapping that maps the children in the layout to their parent.
        # This relationship is calculated dynamically, each time when the UI
        # is rendered.  (UI elements have only references to their children.)
        self._child_to_parent: Dict[Container, Container] = {}

        if focused_element is None:
            try:
                self._stack.append(next(self.find_all_windows()))
            except StopIteration as e:
                raise InvalidLayoutError(
                    "Invalid layout. The layout does not contain any Window object."
                ) from e
        else:
            self.focus(focused_element)

        # List of visible windows.
        self.visible_windows: List[Window] = []  # List of `Window` objects.

    def __repr__(self) -> str:
        return "Layout(%r, current_window=%r)" % (self.container, self.current_window)

    def find_all_windows(self) -> Generator[Window, None, None]:
        """
        Find all the :class:`.UIControl` objects in this layout.
        """
        for item in self.walk():
            if isinstance(item, Window):
                yield item

    def find_all_controls(self) -> Iterable[UIControl]:
        for container in self.find_all_windows():
            yield container.content

    def focus(self, value: FocusableElement) -> None:
        """
        Focus the given UI element.

        `value` can be either:

        - a :class:`.UIControl`
        - a :class:`.Buffer` instance or the name of a :class:`.Buffer`
        - a :class:`.Window`
        - Any container object. In this case we will focus the :class:`.Window`
          from this container that was focused most recent, or the very first
          focusable :class:`.Window` of the container.
        """
        # BufferControl by buffer name.
        if isinstance(value, str):
            for control in self.find_all_controls():
                if isinstance(control, BufferControl) and control.buffer.name == value:
                    self.focus(control)
                    return
            raise ValueError(
                "Couldn't find Buffer in the current layout: %r." % (value,)
            )

        # BufferControl by buffer object.
        elif isinstance(value, Buffer):
            for control in self.find_all_controls():
                if isinstance(control, BufferControl) and control.buffer == value:
                    self.focus(control)
                    return
            raise ValueError(
                "Couldn't find Buffer in the current layout: %r." % (value,)
            )

        # Focus UIControl.
        elif isinstance(value, UIControl):
            if value not in self.find_all_controls():
                raise ValueError(
                    "Invalid value. Container does not appear in the layout."
                )
            if not value.is_focusable():
                raise ValueError("Invalid value. UIControl is not focusable.")

            self.current_control = value

        # Otherwise, expecting any Container object.
        else:
            value = to_container(value)

            if isinstance(value, Window):
                # This is a `Window`: focus that.
                if value not in self.find_all_windows():
                    raise ValueError(
                        "Invalid value. Window does not appear in the layout: %r"
                        % (value,)
                    )

                self.current_window = value
            else:
                # Focus a window in this container.
                # If we have many windows as part of this container, and some
                # of them have been focused before, take the last focused
                # item. (This is very useful when the UI is composed of more
                # complex sub components.)
                windows = []
                for c in walk(value, skip_hidden=True):
                    if isinstance(c, Window) and c.content.is_focusable():
                        windows.append(c)

                # Take the first one that was focused before.
                for w in reversed(self._stack):
                    if w in windows:
                        self.current_window = w
                        return

                # None was focused before: take the very first focusable window.
                if windows:
                    self.current_window = windows[0]
                    return

                raise ValueError(
                    "Invalid value. Container cannot be focused: %r" % (value,)
                )

    def has_focus(self, value: FocusableElement) -> bool:
        """
        Check whether the given control has the focus.
        :param value: :class:`.UIControl` or :class:`.Window` instance.
        """
        if isinstance(value, str):
            if self.current_buffer is None:
                return False
            return self.current_buffer.name == value
        if isinstance(value, Buffer):
            return self.current_buffer == value
        if isinstance(value, UIControl):
            return self.current_control == value
        else:
            value = to_container(value)
            if isinstance(value, Window):
                return self.current_window == value
            else:
                # Check whether this "container" is focused. This is true if
                # one of the elements inside is focused.
                for element in walk(value):
                    if element == self.current_window:
                        return True
                return False

    @property
    def current_control(self) -> UIControl:
        """
        Get the :class:`.UIControl` to currently has the focus.
        """
        return self._stack[-1].content

    @current_control.setter
    def current_control(self, control: UIControl) -> None:
        """
        Set the :class:`.UIControl` to receive the focus.
        """
        for window in self.find_all_windows():
            if window.content == control:
                self.current_window = window
                return

        raise ValueError("Control not found in the user interface.")

    @property
    def current_window(self) -> Window:
        "Return the :class:`.Window` object that is currently focused."
        return self._stack[-1]

    @current_window.setter
    def current_window(self, value: Window) -> None:
        "Set the :class:`.Window` object to be currently focused."
        self._stack.append(value)

    @property
    def is_searching(self) -> bool:
        "True if we are searching right now."
        return self.current_control in self.search_links

    @property
    def search_target_buffer_control(self) -> Optional[BufferControl]:
        """
        Return the :class:`.BufferControl` in which we are searching or `None`.
        """
        # Not every `UIControl` is a `BufferControl`. This only applies to
        # `BufferControl`.
        control = self.current_control

        if isinstance(control, SearchBufferControl):
            return self.search_links.get(control)
        else:
            return None

    def get_focusable_windows(self) -> Iterable[Window]:
        """
        Return all the :class:`.Window` objects which are focusable (in the
        'modal' area).
        """
        for w in self.walk_through_modal_area():
            if isinstance(w, Window) and w.content.is_focusable():
                yield w

    def get_visible_focusable_windows(self) -> List[Window]:
        """
        Return a list of :class:`.Window` objects that are focusable.
        """
        # focusable windows are windows that are visible, but also part of the
        # modal container. Make sure to keep the ordering.
        visible_windows = self.visible_windows
        return [w for w in self.get_focusable_windows() if w in visible_windows]

    @property
    def current_buffer(self) -> Optional[Buffer]:
        """
        The currently focused :class:`~.Buffer` or `None`.
        """
        ui_control = self.current_control
        if isinstance(ui_control, BufferControl):
            return ui_control.buffer
        return None

    def get_buffer_by_name(self, buffer_name: str) -> Optional[Buffer]:
        """
        Look in the layout for a buffer with the given name.
        Return `None` when nothing was found.
        """
        for w in self.walk():
            if isinstance(w, Window) and isinstance(w.content, BufferControl):
                if w.content.buffer.name == buffer_name:
                    return w.content.buffer
        return None

    @property
    def buffer_has_focus(self) -> bool:
        """
        Return `True` if the currently focused control is a
        :class:`.BufferControl`. (For instance, used to determine whether the
        default key bindings should be active or not.)
        """
        ui_control = self.current_control
        return isinstance(ui_control, BufferControl)

    @property
    def previous_control(self) -> UIControl:
        """
        Get the :class:`.UIControl` to previously had the focus.
        """
        try:
            return self._stack[-2].content
        except IndexError:
            return self._stack[-1].content

    def focus_last(self) -> None:
        """
        Give the focus to the last focused control.
        """
        if len(self._stack) > 1:
            self._stack = self._stack[:-1]

    def focus_next(self) -> None:
        """
        Focus the next visible/focusable Window.
        """
        windows = self.get_visible_focusable_windows()

        if len(windows) > 0:
            try:
                index = windows.index(self.current_window)
            except ValueError:
                index = 0
            else:
                index = (index + 1) % len(windows)

            self.focus(windows[index])

    def focus_previous(self) -> None:
        """
        Focus the previous visible/focusable Window.
        """
        windows = self.get_visible_focusable_windows()

        if len(windows) > 0:
            try:
                index = windows.index(self.current_window)
            except ValueError:
                index = 0
            else:
                index = (index - 1) % len(windows)

            self.focus(windows[index])

    def walk(self) -> Iterable[Container]:
        """
        Walk through all the layout nodes (and their children) and yield them.
        """
        for i in walk(self.container):
            yield i

    def walk_through_modal_area(self) -> Iterable[Container]:
        """
        Walk through all the containers which are in the current 'modal' part
        of the layout.
        """
        # Go up in the tree, and find the root. (it will be a part of the
        # layout, if the focus is in a modal part.)
        root: Container = self.current_window
        while not root.is_modal() and root in self._child_to_parent:
            root = self._child_to_parent[root]

        for container in walk(root):
            yield container

    def update_parents_relations(self) -> None:
        """
        Update child->parent relationships mapping.
        """
        parents = {}

        def walk(e: Container) -> None:
            for c in e.get_children():
                parents[c] = e
                walk(c)

        walk(self.container)

        self._child_to_parent = parents

    def reset(self) -> None:
        # Remove all search links when the UI starts.
        # (Important, for instance when control-c is been pressed while
        #  searching. The prompt cancels, but next `run()` call the search
        #  links are still there.)
        self.search_links.clear()

        self.container.reset()

    def get_parent(self, container: Container) -> Optional[Container]:
        """
        Return the parent container for the given container, or ``None``, if it
        wasn't found.
        """
        try:
            return self._child_to_parent[container]
        except KeyError:
            return None


class InvalidLayoutError(Exception):
    pass


def walk(container: Container, skip_hidden: bool = False) -> Iterable[Container]:
    """
    Walk through layout, starting at this container.
    """
    # When `skip_hidden` is set, don't go into disabled ConditionalContainer containers.
    if (
        skip_hidden
        and isinstance(container, ConditionalContainer)
        and not container.filter()
    ):
        return

    yield container

    for c in container.get_children():
        # yield from walk(c)
        yield from walk(c, skip_hidden=skip_hidden)


#################################
class HelpFormatter:
    """This class helps with formatting text-based help pages.  It's
    usually just needed for very special internal cases, but it's also
    exposed so that developers can write their own fancy outputs.

    At present, it always writes into memory.

    :param indent_increment: the additional increment for each level.
    :param width: the width for the text.  This defaults to the terminal
                  width clamped to a maximum of 78.
    """

    def __init__(self, indent_increment=2, width=None, max_width=None):
        self.indent_increment = indent_increment
        if max_width is None:
            max_width = 80
        if width is None:
            width = FORCED_WIDTH
            if width is None:
                width = max(min(terminalsize()[0], max_width) - 2, 50)
        self.width = width
        self.current_indent = 0
        self.buffer = []

    def write(self, string):
        """Writes a unicode string into the internal buffer."""
        self.buffer.append(string)

    def indent(self):
        """Increases the indentation."""
        self.current_indent += self.indent_increment

    def dedent(self):
        """Decreases the indentation."""
        self.current_indent -= self.indent_increment

    def write_usage(self, prog, args="", prefix="Usage: "):
        """Writes a usage line into the buffer.

        :param prog: the program name.
        :param args: whitespace separated list of arguments.
        :param prefix: the prefix for the first line.
        """
        usage_prefix = f"{prefix:>{self.current_indent}}{prog} "
        text_width = self.width - self.current_indent

        if text_width >= (term_len(usage_prefix) + 20):
            # The arguments will fit to the right of the prefix.
            indent = " " * term_len(usage_prefix)
            self.write(
                wraptext(
                    args,
                    text_width,
                    initial_indent=usage_prefix,
                    subsequent_indent=indent,
                )
            )
        else:
            # The prefix is too long, put the arguments on the next line.
            self.write(usage_prefix)
            self.write("\n")
            indent = " " * (max(self.current_indent, term_len(prefix)) + 4)
            self.write(
                wraptext(
                    args, text_width, initial_indent=indent, subsequent_indent=indent
                )
            )

        self.write("\n")

    def write_heading(self, heading):
        """Writes a heading into the buffer."""
        self.write(f"{'':>{self.current_indent}}{heading}:\n")

    def write_paragraph(self):
        """Writes a paragraph into the buffer."""
        if self.buffer:
            self.write("\n")

    def write_text(self, text):
        """Writes re-indented text into the buffer.  This rewraps and
        preserves paragraphs.
        """
        text_width = max(self.width - self.current_indent, 11)
        indent = " " * self.current_indent
        self.write(
            wraptext(
                text,
                text_width,
                initial_indent=indent,
                subsequent_indent=indent,
                preserve_paragraphs=True,
            )
        )
        self.write("\n")

    def write_dl(self, rows, col_max=30, col_spacing=2):
        """Writes a definition list into the buffer.  This is how apps
        and commands are usually formatted.

        :param rows: a list of two item tuples for the terms and values.
        :param col_max: the maximum width of the first column.
        :param col_spacing: the number of spaces between the first and
                            second column.
        """
        rows = list(rows)
        widths = measure_table(rows)
        if len(widths) != 2:
            raise TypeError("Expected two columns for definition list")

        first_col = min(widths[0], col_max) + col_spacing

        for first, second in iter_rows(rows, len(widths)):
            self.write(f"{'':>{self.current_indent}}{first}")
            if not second:
                self.write("\n")
                continue
            if term_len(first) <= first_col - col_spacing:
                self.write(" " * (first_col - term_len(first)))
            else:
                self.write("\n")
                self.write(" " * (first_col + self.current_indent))

            text_width = max(self.width - first_col - 2, 10)
            wrapped_text = wraptext(second, text_width, preserve_paragraphs=True)
            lines = wrapped_text.splitlines()

            if lines:
                self.write(f"{lines[0]}\n")

                for line in lines[1:]:
                    self.write(f"{'':>{first_col + self.current_indent}}{line}\n")

                if len(lines) > 1:
                    # separate long help from next app
                    self.write("\n")
            else:
                self.write("\n")

    @contextmanager
    def section(self, name):
        """Helpful context manager that writes a paragraph, a heading,
        and the indents.

        :param name: the section name that is written as heading.
        """
        self.write_paragraph()
        self.write_heading(name)
        self.indent()
        try:
            yield
        finally:
            self.dedent()

    @contextmanager
    def indentation(self):
        """A context manager that increases the indentation."""
        self.indent()
        try:
            yield
        finally:
            self.dedent()

    def getvalue(self):
        """Returns the buffer contents."""
        return "".join(self.buffer)


def join_apps(apps):
    """Given a list of app strings this joins them in the most appropriate
    way and returns them in the form ``(formatted_string,
    any_prefix_is_slash)`` where the second item in the tuple is a flag that
    indicates if any of the app prefixes was a slash.
    """
    rv = []
    any_prefix_is_slash = False
    for opt in apps:
        prefix = split_opt(opt)[0]
        if prefix == "/":
            any_prefix_is_slash = True
        rv.append((len(prefix), opt))

    rv.sort(key=lambda x: x[0])

    rv = ", ".join(x[1] for x in rv)
    return rv, any_prefix_is_slash
