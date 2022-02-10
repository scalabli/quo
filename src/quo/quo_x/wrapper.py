import os
from ctypes import cdll

libname = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "libcurrentdateandtime.so"))

lib = cdll.LoadLibrary(libname)

class DateTime():
    def __init__(self):
        self.obj = lib.DateTime_new()

    def datetime(self):
        lib.DateTime_datetime(self.obj)
        f = DateTime()
        k = f.datetime
        return k()
