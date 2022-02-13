from quo.prompt import Prompt
from quo.types import Float

session = Prompt()

float(session.prompt("Give me some input", type=Float))
