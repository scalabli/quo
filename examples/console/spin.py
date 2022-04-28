from quo.console import Console

console = Console()

with console.spin():
    import time
    time.sleep(2)
    print("Hello, world")
