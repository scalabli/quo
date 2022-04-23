from quo.text import TextField
#from quo import container
from quo.highlight import HTML

#ontainer(TextField(prompt="djrje", scrollbar=True, hide=False, highlighter=HTML), bind=True)

#from quo.keys import bind


#@bind.add("d")
#ef _(event):
   # event.app.exit()

content = TextField(prompt="djrje", scrollbar=True, hide=False, highlighter=HTML)

#container(content, bind=True)

print("hello "+ content.text)
