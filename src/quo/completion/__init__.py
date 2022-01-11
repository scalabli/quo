from .core import (
    CompleteEvent,
    CompleteStyle,
    Completer,
    Completion,
    ConditionalCompleter,
    DummyCompleter,
    DynamicCompleter,
    ThreadedCompleter,
    get_common_complete_suffix,
    merge_completers,
)
#from quo.shortcuts.prompt import CompleStyle
from .deduplicate import DeduplicateCompleter
from .filesystem import ExecutableCompleter, PathCompleter
from .fuzzy_completer import FuzzyCompleter, FuzzyWordCompleter
from .nested import NestedCompleter
from .word_completer import WordCompleter
from .auto_suggest import AutoSuggestFromHistory

__all__ = [
    # Base.
    "Completion",
    "Completer",
    "ThreadedCompleter",
    "DummyCompleter",
    "DynamicCompleter",
    "CompleteEvent",
    "ConditionalCompleter",
    "merge_completers",
    "get_common_complete_suffix",
    # Filesystem.
    "PathCompleter",
    "ExecutableCompleter",
    # Fuzzy
    "FuzzyCompleter",
    "FuzzyWordCompleter",
    # Nested.
    "NestedCompleter",
    # Word completer.
    "WordCompleter",
    # Deduplicate
    "DeduplicateCompleter",
]
