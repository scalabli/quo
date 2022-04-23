from quo.console import Console

console = Console()

#stdout = console.openfile('-', 'w')

with console.open('/root/ds/news.py', 'a') as f:
    f.write("ddffdd\n")

#print(test_file)
