# AUTOGENERATED! DO NOT EDIT! File to edit: 01_decorator.ipynb (unless otherwise specified).

__all__ = ['os', 'sys', 'ForkingUnixServer', 'fastcgi']

# Cell
from .core import FcgiHandler,TextWrapper
from fastcore.basics import *
from fastcore.imports import *
from socketserver import UnixStreamServer,TCPServer,ForkingMixIn,ForkingTCPServer
import inspect,os,sys

# Cell
#nbdev_comment _all_ = ['os','sys']

# Cell
class ForkingUnixServer(ForkingMixIn, UnixStreamServer): pass

# Cell
def fastcgi(sock='fcgi.sock', func=None):
    if callable(sock): sock,func = 'fcgi.sock',sock
    if isinstance(sock,Path): sock = str(sock)
    if func is None: return partial(fastcgi, sock)

    mod = inspect.getmodule(inspect.currentframe().f_back)
    class DecorateHandler(FcgiHandler):
        def handle(self):
            oldin,oldout,oldenv = sys.stdin,sys.stdout,os.environ
            try:
                sys.stdin,sys.stdout,os.environ = TextWrapper(self['stdin']),TextWrapper(self['stdout']),self.environ
                func()
            finally: sys.stdin,sys.stdout,os.environ = oldin,oldout,oldenv

    srv_type = ForkingUnixServer if isinstance(sock,str) else ForkingTCPServer
    f = partial(srv_type, sock, DecorateHandler)
    if mod and mod.__name__=="__main__":
        if isinstance(sock,str) and os.path.exists(sock): os.unlink(sock)
        try:
            with f() as srv: srv.serve_forever()
        except KeyboardInterrupt:
            if isinstance(sock,str):os.unlink(sock)
    else: return f