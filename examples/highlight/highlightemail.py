from quo.highlight import Highlight
from quo.prompt import Prompt

session = Prompt(highlighter=Highlight.email)

session.prompt()