from quo import echo, launch
echo(f"If your terminal supports links, the following text should be launchable:")

link = "https://quo.rtfd.io"
echo(f"Quo's documentation", fg="green")
launch(link)
