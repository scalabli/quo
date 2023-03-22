from quo import container
from quo.widget import Frame


root = Frame(title="Quo: python")
       
container(root, bind=True, full_screen=True)                           
