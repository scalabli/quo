from ctypes import cdll
lib = cdll.LoadLibrary('./AppNotFound.so')



class AppNotFound():
    def __init__(self):
        self.obj = lib.App_error()

    def app_error(self):
        lib.AppNotFound(self.obj)
