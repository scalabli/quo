from quo.parse import Parser

parser = Parser()
group = parser.group()
group.argument("-v", "--verbose", action="store_true")
group.argument("-q", "--quiet", action="store_true")
parser.argument("x", type=int, help="the base")
parser.argument("y", type=int, help="the exponent")
arg = parser.parse()
answer = arg.x**arg.y

if arg.quiet:
    print(answer)
elif arg.verbose:
    print(f"{arg.x} to the power {arg.y} equals {answer}")
else:
    print(f"{arg.x}^{arg.y} == {answer}")