import quo
from quo import prompt, flair
answer = prompt("How old are you?")
flair(f"I am: {answer}", fg="cyan")
