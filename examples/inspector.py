from quo.console import Console

import inspect
  
# create classes
class A(object):
    pass
  
class B(A):
    pass
  
class C(B):
    pass
  

print(inspect.getdoc(Console()))
# nested list of tuples
for i in (inspect.getclasstree(inspect.getmro(Console))):
    print(i)


