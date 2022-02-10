import os
from ctypes import cdll

libname = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "liberror1.so"))

lib = cdll.LoadLibrary(libname)

class AppNotFound():
    def __init__(self):
        self.obj = lib.AppNotFound_new()

    def error(self):
        lib.AppNotFound_error(self.obj)
