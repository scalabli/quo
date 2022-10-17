"""
Lexer interface and implementations.
Used for syntax highlighting.
"""

#from .core import DynamicLexer, Lexer, SimpleLexer
#from .pygments import RegexSync, SyncFromStart, SyntaxSync


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


class Highlight:

    from .pygments import PygmentsLexer

    _CSS = []
    match _CSS:
        case css:
             from pygments.lexers.css import CssLexer
             css = PygmentsLexer(CssLexer)

    _EMAIL = []
    match _EMAIL:
        case email:
            from pygments.lexers.email import EmailLexer
            email = PygmentsLexer(EmailLexer)

    _FORTRAN = []
    match _FORTRAN:
        case fortran:
            from pygments.lexers.fortran import FortranLexer
            fortran = PygmentsLexer(FortranLexer)

    _GO = []
    match _GO:
        case go:
            from pygments.lexers.go import GoLexer
            go = PygmentsLexer(GoLexer)


    _HASKELL = []
    match _HASKELL:
        case haskell:
             from pygments.lexers.haskell import HaskellLexer
             haskell = PygmentsLexer(HaskellLexer)

    _HTML = []
    match _HTML:
        case html:
            from pygments.lexers.html import HtmlLexer
            html = PygmentsLexer(HtmlLexer)


    _PYTHON = []
    match _PYTHON:
        case python:
            from pygments.lexers.python import PythonLexer
            python = PygmentsLexer(PythonLexer)

    _RUBY = []
    match _RUBY:
        case ruby:
            from pygments.lexers.ruby import RubyLexer
            ruby = PygmentsLexer(RubyLexer)

    _RUST = []
    match _RUST:
        case rust:
            from pygments.lexers.rust import RustLexer
            rust = PygmentsLexer(RustLexer)

    _SHELL = []
    match _SHELL:
        case shell:
            from pygments.lexers.shell import BashLexer
            shell = PygmentsLexer(BashLexer)
            
            
    _SOLIDITY = []
    match _SOLIDITY:
        case solidity:
            from pygments.lexers.solidity import SolidityLexer
            solidity = PygmentsLexer(SolidityLexer)

    _SQL = []
    match _SQL:
        case sql:
            from pygments.lexers.sql import SqlLexer
            sql = PygmentsLexer(SqlLexer)





            
#:TODO: Add more lexers



   



# sas.py
# scdoc.py
# scripting.py
# sgf.py   

# special.py

# snobol.py
# Actionscript
##from pygments.lexers.actionscript import ActionScriptLexer as ActionLexer

#actionscript = PygmentsLexer(ActionLexer)
# agile = PygmentsLexer(CL)
# algebra = PygmentsLexer(CL)
# ambient = PygmentsLexer(CL)
# ampl = PygmentsLexer(CL)
# apl = PygmentsLexer(CL)
# archetype = PygmentsLexer(CL)

#from pygments.lexers.arrow import ArrowLexer as ArrowL

#arrow = PygmentsLexer(ArrowL)
# asm = PygmentsLexer(CL)
##from pygments.lexers.automation import AutohotkeyLexer as AutomationL

##automation = PygmentsLexer(AutomationL)

# bare.py
# basic.py
# bibtex
#from pygments.lexers.bibtex import BibTeXLexer as BibL

##bibtex = PygmentsLexer(BibL)
#Bibtex = bibtex
# boa.py

#from pygments.lexers.c_cpp import CFamilyLexer as C_Lexer



#cpp = PygmentsLexer(C_Lexer)
#Cpp = cpp
#CPP = cpp

# c_like.py
# capnproto.py
# chapel.py
# clean.py
# compiled.py
# configs.py
# console.py
# crystal.py

# dalvik.py
# data.py
# devicetree.py
# diff.py
# dotnet.py
# dsls.p




# erlang.py
# esoteric.py
# ezhil.py
# factor.py
# fantom.py
# felix.py
# floscript.py
# forth.py


# gdscript.py


# grammar_notation.py
# graph.py
# graphics.py


# haxe.py
# hdl.py
# hexdump.py

# int_fiction.py
# iolang.py
# j.py
# Javascript
#from pygments.lexers.javascript import JavascriptLexer as JavasL

#javascript = PygmentsLexer(JavasL)
#Javascript = javascript
# Julia
#from pygments.lexers.julia import JuliaLexer

#julia = PygmentsLexer(JuliaLexer)
#Julia = julia
# jvm.py
# lisp.py
# make.py
# markup.py
# math.py
# matlab.py
# mime.py
# ml.py
# modeling.py
# modula2.py
# monte.py
# mosel.py
# ncl.py
# nimrod.py
# nit.py
# nix.py
# oberon.py

# pascal.py
# pawn.py
#from pygments.lexers.perl import PerlLexer

#perl = PygmentsLexer(EmailL)
#Perl = perl

#from pygments.lexers.php import PhpLexer

#php = PygmentsLexer(PhpLexer)
#Php = php
#PHP = php

# r.py
# rdf.py


# stata.py

# usd
