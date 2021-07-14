from quo import prompt, flair, echo

ans = prompt(flair(f"@input", fg="red", bg="white"))
flair(f"{ans}", fg="cyan", bold=True)
