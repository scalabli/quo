from quo.prompt import Prompt

session = Prompt()

session.prompt('> ', bottom_toolbar="<i>This is a</i><b><style bg='red'> Toolbar</style></b>")
