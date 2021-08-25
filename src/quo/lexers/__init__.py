"""
Lexer interface and implementations.
Used for syntax highlighting.
"""
from .core import DynamicLexer, Lexer, SimpleLexer
from .pygments import PygmentsLexer, RegexSync, SyncFromStart, SyntaxSync

__all__ = [
    # Core
    "Lexer",
    "SimpleLexer",
    "DynamicLexer",
    # Pygments.
    "PygmentsLexer",
    "RegexSync",
    "SyncFromStart",
    "SyntaxSync",
]
