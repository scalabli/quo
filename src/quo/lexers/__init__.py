"""
Lexer interface and implementations.
Used for syntax highlighting.
"""
from .core import (
        DynamicLexer,
        Lexer, 
        SimpleLexer
        )

from .pygments import (
        PygmentsLexer,
        RegexSync, 
        SyncFromStart,
        SyntaxSync
        )

__all__ = [
    "Lexer",
    "SimpleLexer",
    "DynamicLexer",
    "PygmentsLexer",
    "RegexSync",
    "SyncFromStart",
    "SyntaxSync",
]
