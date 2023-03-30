from quo import container
from quo.textfield import TextField



textfield = TextField(hide=True, bg="black", fg="red")

container(textfield, bind=True, full_screen=True)