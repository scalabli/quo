import typing

from ._loop import loop_first, loop_last
from quo.console.console import Console, ConsoleOptions, RenderableType, RenderResult
from .jupyter import JupyterMixin
from quo.measure.measure import Measurement
from .segment import Segment
from .style import Style, StyleStack
from .styled import Styled

StyleType = typing.Union[str, "Style"]

class Tree(JupyterMixin):
    """A renderable for a tree structure.

    Args:
        label (RenderableType): The renderable or str for the tree label.
        style (StyleType, optional): Style of this tree. Defaults to "tree".
        guide_style (StyleType, optional): Style of the guide lines. Defaults to "tree.line".
        expanded (bool, optional): Also display children. Defaults to True.
        highlight (bool, optional): Highlight renderable (if str). Defaults to False.
    """

    def __init__(
        self,
        label: RenderableType,
        *,
        style: StyleType = "tree",
        guide_style: StyleType = "tree.line",
        expanded: bool = True,
        highlight: bool = False,
    ) -> None:
        self.label = label
        self.style = style
        self.guide_style = guide_style
        self.children: List[Tree] = []
        self.expanded = expanded
        self.highlight = highlight

    def add(
        self,
        label: RenderableType,
        *,
        style: typing.Optional[StyleType] = None,
        guide_style: typing.Optional[StyleType] = None,
        expanded: bool = True,
        highlight: bool = False,
    ) -> "Tree":
        """Add a child tree.

        Args:
            label (RenderableType): The renderable or str for the tree label.
            style (StyleType, optional): Style of this tree. Defaults to "tree".
            guide_style (StyleType, optional): Style of the guide lines. Defaults to "tree.line".
            expanded (bool, optional): Also display children. Defaults to True.
            highlight (Optional[bool], optional): Highlight renderable (if str). Defaults to False.

        Returns:
            Tree: A new child Tree, which may be further modified.
        """
        node = Tree(
            label,
            style=self.style if style is None else style,
            guide_style=self.guide_style if guide_style is None else guide_style,
            expanded=expanded,
            highlight=self.highlight if highlight is None else highlight,
        )
        self.children.append(node)
        return node

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        stack: typing.List[typing.Iterator[typing.Tuple[bool, Tree]]] = []
        pop = stack.pop
        push = stack.append
        new_line = Segment.line()

        get_style = console.get_style
        null_style = Style.null()
        guide_style = get_style(self.guide_style, default="") or null_style
        SPACE, CONTINUE, FORK, END = range(4)

        ASCII_GUIDES = ("    ", "|   ", "+-- ", "`-- ")
        TREE_GUIDES = [
            ("    ", "│   ", "├── ", "└── "),
            ("    ", "┃   ", "┣━━ ", "┗━━ "),
            ("    ", "║   ", "╠══ ", "╚══ "),
        ]
        _Segment = Segment

        def make_guide(index: int, style: Style) -> Segment:
            """Make a Segment for a level of the guide lines."""
            if options.ascii_only:
                line = ASCII_GUIDES[index]
            else:
                guide = 1 if style.bold else (2 if style.underline2 else 0)
                line = TREE_GUIDES[0 if options.legacy_windows else guide][index]
            return _Segment(line, style)

        levels: typing.List[Segment] = [make_guide(CONTINUE, guide_style)]
        push(iter(loop_last([self])))

        guide_style_stack = StyleStack(get_style(self.guide_style))
        style_stack = StyleStack(get_style(self.style))
        remove_guide_styles = Style(bold=False, underline2=False)

        while stack:
            stack_node = pop()
            try:
                last, node = next(stack_node)
            except StopIteration:
                levels.pop()
                if levels:
                    guide_style = levels[-1].style or null_style
                    levels[-1] = make_guide(FORK, guide_style)
                    guide_style_stack.pop()
                    style_stack.pop()
                continue
            push(stack_node)
            if last:
                levels[-1] = make_guide(END, levels[-1].style or null_style)

            guide_style = guide_style_stack.current + get_style(node.guide_style)
            style = style_stack.current + get_style(node.style)
            prefix = levels[1:]
            renderable_lines = console.render_lines(
                Styled(node.label, style),
                options.update(
                    width=options.max_width
                    - sum(level.cell_length for level in prefix),
                    highlight=self.highlight,
                    height=None,
                ),
            )
            for first, line in loop_first(renderable_lines):
                if prefix:
                    yield from _Segment.apply_style(
                        prefix,
                        style.background_style,
                        post_style=remove_guide_styles,
                    )
                yield from line
                yield new_line
                if first and prefix:
                    prefix[-1] = make_guide(
                        SPACE if last else CONTINUE, prefix[-1].style or null_style
                    )

            if node.expanded and node.children:
                levels[-1] = make_guide(
                    SPACE if last else CONTINUE, levels[-1].style or null_style
                )
                levels.append(
                    make_guide(END if len(node.children) == 1 else FORK, guide_style)
                )
                style_stack.push(get_style(node.style))
                guide_style_stack.push(get_style(node.guide_style))
                push(iter(loop_last(node.children)))

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "Measurement":
        stack: typing.List[typing.Iterator[Tree]] = [iter([self])]
        pop = stack.pop
        push = stack.append
        minimum = 0
        maximum = 0
        measure = Measurement.get
        level = 0
        while stack:
            iter_tree = pop()
            try:
                tree = next(iter_tree)
            except StopIteration:
                level -= 1
                continue
            push(iter_tree)
            min_measure, max_measure = measure(console, options, tree.label)
            indent = level * 4
            minimum = max(min_measure + indent, minimum)
            maximum = max(max_measure + indent, maximum)
            if tree.expanded and tree.children:
                push(iter(tree.children))
                level += 1
        return Measurement(minimum, maximum)
