import os
import inspect
import importlib
class Reloader:

    def __init__(self,fn):
        self.sf = inspect.getsourcefile(fn)
        self.mn = inspect.getmodulename(self.sf)
        self.fn = fn
        self.last = os.stat(self.sf).st_mtime_ns

    def exec(self,*args,**kwargs):
        t = os.stat(self.sf).st_mtime_ns        
        if t != self.last:
            self.last = t
            mod = importlib.import_module(self.mn)
            self.reload(mod)
            print("Reload")
        return self.fn(*args, **kwargs)

    def reload(self,mod):
        importlib.reload(mod)
        for m in dir(mod):
            if inspect.ismodule(m):
                self.reload(m)

