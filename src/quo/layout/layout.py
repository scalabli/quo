"""
Wrapper for the layout.
"""

import typing as t


from quo.errors import exceptions
from .utils import Buffer

from .containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    Window,
    to_container,
)
from .controls import (
        BufferControl,
        SearchBufferControl,
        UIControl
        )

__all__ = [
    "Layout",
    "InvalidLayoutError",
    "walk",
]

FocusableElement = t.Union[str, Buffer, UIControl, AnyContainer]


class Layout:
    """
    The layout for a quo
    :class:`~quo.Suite`.
    This also keeps track of which user control is focused.

    :param container: The "root" container for the layout.
    :param focused_element: element to be focused initially. (Can be anything
        the `focus` function accepts.)
    """

    def __init__(
        self,
        container: AnyContainer,
        focused_element: t.Optional[FocusableElement] = None,
    ) -> None:

        self.container = to_container(container)
        self._stack: t.List[Window] = []

        # Map search BufferControl back to the original BufferControl.
        # This is used to keep track of when exactly we are searching, and for
        # applying the search.
        # When a link exists in this dictionary, that means the search is
        # currently active.
        # Map: search_buffer_control -> original buffer control.
        self.search_links: t.Dict[SearchBufferControl, BufferControl] = {}

        # Mapping that maps the children in the layout to their parent.
        # This relationship is calculated dynamically, each time when the UI
        # is rendered.  (UI elements have only references to their children.)
        self._child_to_parent: t.Dict[Container, Container] = {}

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
        self.visible_windows: t.List[Window] = []  # List of `Window` objects.

    def __repr__(self) -> str:
        return "Layout(%r, current_window=%r)" % (self.container, self.current_window)

    def find_all_windows(self) -> t.Generator[Window, None, None]:
        """
        Find all the :class:`.UIControl` objects in this layout.
        """
        for item in self.walk():
            if isinstance(item, Window):
                yield item

    def find_all_controls(self) -> t.Iterable[UIControl]:
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
    def search_target_buffer_control(self) -> t.Optional[BufferControl]:
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

    def get_focusable_windows(self) -> t.Iterable[Window]:
        """
        Return all the :class:`.Window` objects which are focusable (in the
        'modal' area).
        """
        for w in self.walk_through_modal_area():
            if isinstance(w, Window) and w.content.is_focusable():
                yield w

    def get_visible_focusable_windows(self) -> t.List[Window]:
        """
        Return a list of :class:`.Window` objects that are focusable.
        """
        # focusable windows are windows that are visible, but also part of the
        # modal container. Make sure to keep the ordering.
        visible_windows = self.visible_windows
        return [w for w in self.get_focusable_windows() if w in visible_windows]

    @property
    def current_buffer(self) -> t.Optional[Buffer]:
        """
        The currently focused :class:`~.Buffer` or `None`.
        """
        ui_control = self.current_control
        if isinstance(ui_control, BufferControl):
            return ui_control.buffer
        return None

    def get_buffer_by_name(self, buffer_name: str) -> t.Optional[Buffer]:
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

    def walk(self) -> t.Iterable[Container]:
        """
        Walk through all the layout nodes (and their children) and yield them.
        """
        for i in walk(self.container):
            yield i

    def walk_through_modal_area(self) -> t.Iterable[Container]:
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

    def get_parent(self, container: Container) -> t.Optional[Container]:
        """
        Return the parent container for the given container, or ``None``, if it
        wasn't found.
        """
        try:
            return self._child_to_parent[container]
        except KeyError:
            return None


def walk(container: Container, skip_hidden: bool = False) -> t.Iterable[Container]:
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


from itertools import islice
from operator import itemgetter
from quo._ratio import ratio_resolve
from quo.align import Align
from quo.console.console import Console, ConsoleOptions, RenderableType, RenderResult
from quo.highlighter import ReprHighlighter
from quo.panel import Panel
from quo.pretty import Pretty
from quo.repr import rich_repr, Result
from quo.region import Region
from quo.segment import Segment
from quo.style import Style

if t.TYPE_CHECKING:
    from quo.tree import Tree

StyleType = t.Union[str, "Style"]

class LayoutRender(t.NamedTuple):
    """An individual layout render."""

    region: Region
    render: t.List[t.List[Segment]]


RegionMap = t.Dict["Layout", Region]
RenderMap = t.Dict["Layout", LayoutRender]


class NoSplitter(exceptions.LayoutError):
    """Requested splitter does not exist."""


class _Placeholder:
    """An internal renderable used as a Layout placeholder."""

    highlighter = ReprHighlighter()

    def __init__(self, layout: "Outline", style: StyleType = "") -> None:
        self.layout = layout
        self.style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width
        height = options.height or options.size.height
        layout = self.layout
        title = (
            f"{layout.name!r} ({width} x {height})"
            if layout.name
            else f"({width} x {height})"
        )
        yield Panel(
            Align.center(Pretty(layout), vertical="middle"),
            style=self.style,
            title=self.highlighter(title),
            border_style="blue",
        )

import abc

class Splitter(abc.ABC):
    """Base class for a splitter."""

    name: str = ""

    @abc.abstractmethod
    def get_tree_icon(self) -> str:
        """Get the icon (emoji) used in layout.tree"""

    @abc.abstractmethod
    def divide(
        self, children: t.Sequence["Outline"], region: Region
    ) -> t.Iterable[t.Tuple["Outline", Region]]:
        """Divide a region amongst several child outlines

        Args:
            children (Sequence(Layout)): A number of child layouts.
            region (Region): A rectangular region to divide.
        """


class RowSplitter(Splitter):
    """Split a layout region in to rows."""

    name = "row"

    def get_tree_icon(self) -> str:
        return "[layout.tree.row]⬌"

    def divide(
        self, children: t.Sequence["Layout"], region: Region
    ) -> t.Iterable[t.Tuple["Outline", Region]]:
        x, y, width, height = region
        render_widths = ratio_resolve(width, children)
        offset = 0
        _Region = Region
        for child, child_width in zip(children, render_widths):
            yield child, _Region(x + offset, y, child_width, height)
            offset += child_width


class ColumnSplitter(Splitter):
    """Split a layout region in to columns."""

    name = "column"

    def get_tree_icon(self) -> str:
        return "[layout.tree.column]⬍"

    def divide(
        self, children: t.Sequence["Outline"], region: Region
    ) -> t.Iterable[t.Tuple["Outline", Region]]:
        x, y, width, height = region
        render_heights = ratio_resolve(height, children)
        offset = 0
        _Region = Region
        for child, child_height in zip(children, render_heights):
            yield child, _Region(x, y + offset, width, child_height)
            offset += child_height

from threading import RLock

@rich_repr
class Outline:

    """A renderable to divide a fixed height in to rows or columns.

    Args:
        renderable (RenderableType, optional): Renderable content, or None for placeholder. Defaults to None.
        name (str, optional): Optional identifier for Layout. Defaults to None.
        size (int, optional): Optional fixed size of layout. Defaults to None.
        minimum_size (int, optional): Minimum size of layout. Defaults to 1.
        ratio (int, optional): Optional ratio for flexible layout. Defaults to 1.
        visible (bool, optional): Visibility of layout. Defaults to True.
    """

    splitters = {"row": RowSplitter, "column": ColumnSplitter}

    def __init__(
        self,
        renderable: t.Optional[RenderableType] = None,
        *,
        name: t.Optional[str] = None,
        size: t.Optional[int] = None,
        minimum_size: int = 1,
        ratio: int = 1,
        visible: bool = True,
        height: t.Optional[int] = None,
    ) -> None:
        self._renderable = renderable or _Placeholder(self)
        self.size = size
        self.minimum_size = minimum_size
        self.ratio = ratio
        self.name = name
        self.visible = visible
        self.height = height
        self.splitter: Splitter = self.splitters["column"]()
        self._children: t.List[Layout] = []
        self._render_map: RenderMap = {}
        self._lock = RLock()

    def __rich_repr__(self) -> Result:
        yield "name", self.name, None
        yield "size", self.size, None
        yield "minimum_size", self.minimum_size, 1
        yield "ratio", self.ratio, 1

    @property
    def renderable(self) -> RenderableType:
        """Layout renderable."""
        return self if self._children else self._renderable

    @property
    def children(self) -> t.List["Layout"]:
        """Gets (visible) layout children."""
        return [child for child in self._children if child.visible]

    @property
    def map(self) -> RenderMap:
        """Get a map of the last render."""
        return self._render_map

    def get(self, name: str) -> t.Optional["Outline"]:
        """Get a named layout/outline, or None if it doesn't exist.

        Args:
            name (str): Name of layout.

        Returns:
            Optional[Layout]: Layout instance or None if no layout was found.
        """
        if self.name == name:
            return self
        else:
            for child in self._children:
                named_layout = child.get(name)
                if named_layout is not None:
                    return named_layout
        return None

    def __getitem__(self, name: str) -> "Layout":
        layout = self.get(name)
        if layout is None:
            raise KeyError(f"No layout with name {name!r}")
        return layout

    @property
    def tree(self) -> "Tree":
        """Get a tree renderable to show layout structure."""
        from quo.styled import Styled
        from quo.table import Table
        from quo.tree import Tree

        def summary(layout: "Outline") -> Table:

            icon = layout.splitter.get_tree_icon()

            table = Table.grid(padding=(0, 1, 0, 0))

            text: RenderableType = (
                Pretty(layout) if layout.visible else Styled(Pretty(layout), "dim")
            )
            table.add_row(icon, text)
            _summary = table
            return _summary

        layout = self
        tree = Tree(
            summary(layout),
            guide_style=f"layout.tree.{layout.splitter.name}",
            highlight=True,
        )

        def recurse(tree: "Tree", layout: "Outline") -> None:
            for child in layout._children:
                recurse(
                    tree.add(
                        summary(child),
                        guide_style=f"layout.tree.{child.splitter.name}",
                    ),
                    child,
                )

        recurse(tree, self)
        return tree

    def split(
        self,
        *layouts: t.Union["Outline", RenderableType],
        splitter: t.Union[Splitter, str] = "column",
    ) -> None:
        """Split the layout in to multiple sub-layouts.

        Args:
            *layouts (Layout): Positional arguments should be (sub) Layout instances.
            splitter (Union[Splitter, str]): Splitter instance or name of splitter.
        """
        _layouts = [
            layout if isinstance(layout, Outline) else Outline(layout)
            for layout in layouts
        ]
        try:
            self.splitter = (
                splitter
                if isinstance(splitter, Splitter)
                else self.splitters[splitter]()
            )
        except KeyError:
            raise NoSplitter(f"No splitter called {splitter!r}")
        self._children[:] = _layouts

    def add_split(self, *layouts: t.Union["Layout", RenderableType]) -> None:
        """Add a new layout(s) to existing split.

        Args:
            *layouts (Union[Layout, RenderableType]): Positional arguments should be renderables or (sub) Layout instances.

        """
        _layouts = (
            layout if isinstance(layout, Outline) else Outline(layout)
            for layout in layouts
        )
        self._children.extend(_layouts)

    def split_row(self, *layouts: t.Union["Outline", RenderableType]) -> None:
        """Split the layout in tow a row (Layouts side by side).

        Args:
            *layouts (Layout): Positional arguments should be (sub) Layout instances.
        """
        self.split(*layouts, splitter="row")

    def split_column(self, *layouts: t.Union["Outline", RenderableType]) -> None:
        """Split the layout in to a column (layouts stacked on top of each other).

        Args:
            *layouts (Layout): Positional arguments should be (sub) Layout instances.
        """
        self.split(*layouts, splitter="column")

    def unsplit(self) -> None:
        """Reset splits to initial state."""
        del self._children[:]

    def update(self, renderable: RenderableType) -> None:
        """Update renderable.

        Args:
            renderable (RenderableType): New renderable object.
        """
        with self._lock:
            self._renderable = renderable

    def refresh_screen(self, console: "Console", layout_name: str) -> None:
        """Refresh a sub-layout.

        Args:
            console (Console): Console instance where Layout is to be rendered.
            layout_name (str): Name of layout.
        """
        with self._lock:
            layout = self[layout_name]
            region, _lines = self._render_map[layout]
            (x, y, width, height) = region
            lines = console.render_lines(
                layout, console.options.update_dimensions(width, height)
            )
            self._render_map[layout] = LayoutRender(region, lines)
            console.update_screen_lines(lines, x, y)

    def _make_region_map(self, width: int, height: int) -> RegionMap:
        """Create a dict that maps layout on to Region."""
        stack: t.List[t.Tuple[Outline, Region]] = [(self, Region(0, 0, width, height))]
        push = stack.append
        pop = stack.pop
        layout_regions: t.List[t.Tuple[Outline, Region]] = []
        append_layout_region = layout_regions.append
        while stack:
            append_layout_region(pop())
            layout, region = layout_regions[-1]
            children = layout.children
            if children:
                for child_and_region in layout.splitter.divide(children, region):
                    push(child_and_region)

        region_map = {
            layout: region
            for layout, region in sorted(layout_regions, key=itemgetter(1))
        }
        return region_map

    def render(self, console: Console, options: ConsoleOptions) -> RenderMap:
        """Render the sub_layouts.

        Args:
            console (Console): Console instance.
            options (ConsoleOptions): Console options.

        Returns:
            RenderMap: A dict that maps Layout on to a tuple of Region, lines
        """
        render_width = options.max_width
        render_height = options.height or console.height
        region_map = self._make_region_map(render_width, render_height)
        layout_regions = [
            (layout, region)
            for layout, region in region_map.items()
            if not layout.children
        ]
        render_map: t.Dict["Layout", "LayoutRender"] = {}
        render_lines = console.render_lines
        update_dimensions = options.update_dimensions

        for layout, region in layout_regions:
            lines = render_lines(
                layout.renderable, update_dimensions(region.width, region.height)
            )
            render_map[layout] = LayoutRender(region, lines)
        return render_map

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        with self._lock:
            width = options.max_width or console.width
            height = options.height or console.height
            render_map = self.render(console, options.update_dimensions(width, height))
            self._render_map = render_map
            layout_lines: t.List[t.List[Segment]] = [[] for _ in range(height)]
            _islice = islice
            for (region, lines) in render_map.values():
                _x, y, _layout_width, layout_height = region
                for row, line in zip(
                    _islice(layout_lines, y, y + layout_height), lines
                ):
                    row.extend(line)

            new_line = Segment.line()
            for layout_row in layout_lines:
                yield from layout_row
                yield new_line
