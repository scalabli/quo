from quo.parse import Parser

optional = Parser()
optional.argument("--verbosity", help="Increase the verbosity")
arg = optional.parse()
if arg.verbosity:
    print("Verbosity turned on")
