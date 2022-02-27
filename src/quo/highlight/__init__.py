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


from pygments.lexers.html import HtmlLexer as HL
HTML = PygmentsLexer(HL)
html = HTML

from pygments.lexers.python import PythonLexer as PL
Python = PygmentsLexer(PL)

from pygments.lexers.css import CssLexer as CL
css = PygmentsLexer(CL)
CSS = css
Css = css

# Actionscript
from pygments.lexers.actionscript import ActionScriptLexer as ActionLexer
actionscript = PygmentsLexer(ActionLexer)
#agile = PygmentsLexer(CL)
#algebra = PygmentsLexer(CL)
#ambient = PygmentsLexer(CL)
#ampl = PygmentsLexer(CL)
#apl = PygmentsLexer(CL)
#archetype = PygmentsLexer(CL)

from pygments.lexers.arrow import ArrowLexer as ArrowL
arrow = PygmentsLexer(ArrowL)
#asm = PygmentsLexer(CL)
from pygments.lexers.automation import AutohotkeyLexer  as AutomationL
automation = PygmentsLexer(AutomationL)

#bare.py
#basic.py
#bibtex
from pygments.lexers.bibtex import BibTeXLexer as BibL
bibtex = PygmentsLexer(BibL)
Bibtex = bibtex
#boa.py

from pygments.lexers.c_cpp import CFamilyLexer as C_Lexer
cpp = PygmentsLexer(C_Lexer)
Cpp = cpp
CPP = cpp

#c_like.py
#capnproto.py
#chapel.py
#clean.py
#compiled.py
#configs.py
#console.py
#crystal.py

#dalvik.py
#data.py
#devicetree.py
#diff.py
#dotnet.py
#dsls.p
from pygments.lexers.email import EmailLexer as EmailL
email = PygmentsLexer(EmailL)
Email = email

#erlang.py
#esoteric.py
#ezhil.py
#factor.py
#fantom.py
#felix.py
#floscript.py
#forth.py
from pygments.lexers.fortran import FortranLexer as FortL
fortran = PygmentsLexer(FortL)
Fortran = fortran

#gdscript.py
from pygments.lexers.go import GoLexer as GoL
go = PygmentsLexer(GoL)
Go = go


#grammar_notation.py
#graph.py
#graphics.py

from pygments.lexers.haskell import HaskellLexer as HaskellL
haskell = PygmentsLexer(HaskellL)
Haskell = haskell
#haxe.py
#hdl.py
#hexdump.py

#int_fiction.py
#iolang.py
#j.py
# Javascript
from pygments.lexers.javascript import JavascriptLexer as JavasL
javascript = PygmentsLexer(JavasL)
Javascript = javascript
# Julia
from pygments.lexers.julia import JuliaLexer
julia = PygmentsLexer(JuliaLexer)
Julia = julia
#jvm.py
#lisp.py
#make.py
#markup.py
#math.py
#matlab.py
#mime.py
#ml.py
#modeling.py
#modula2.py
#monte.py
#mosel.py
#ncl.py
#nimrod.py
#nit.py
#nix.py
#oberon.py

#pascal.py
#pawn.py
#perl
from pygments.lexers.perl import PerlLexer
perl = PygmentsLexer(EmailL)
Perl = perl

#php
from pygments.lexers.php import PhpLexer
php =  PygmentsLexer(PhpLexer)
Php = php
PHP = php

#r.py
#rdf.py

#ruby
from pygments.lexers.ruby import RubyLexer
ruby = PygmentsLexer(RubyLexer)
Ruby = ruby

#rust
from pygments.lexers.rust import RustLexer
rust = PygmentsLexer(RustLexer)
Rust = rust
#sas.py
#scdoc.py
#scripting.py
#sgf.py
#shell
from pygments.lexers.shell import BashLexer
shell = PygmentsLexer(BashLexer)
Shell = shell

#snobol.py
#solidity
from pygments.lexers.solidity import SolidityLexer
solidity = PygmentsLexer(SolidityLexer)
Solidity = solidity

#special.py

#sql
from pygments.lexers.sql import SqlLexer
sql = PygmentsLexer(SqlLexer)
Sql = sql
SQL = sql

#stata.py

#usd


