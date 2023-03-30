from quo import container
from quo.widget import TextField


with open("/root/git/quo/examples/full-screen/full-screen-demo.py", "rb") as f:
    text = f.read().decode("utf-8")


content = TextField(text, multiline=True)

container(content)
