from functools import *
import pdb
import playground

"""
NOTES
keyed_objects only need to implement get_key.  
convention: will only call function using keyworded arguments
note: not using functional programming for these objects.  instead, am binding get_key functions to each class of keyed_objects
note: have accepted that the same function call with or without partial will have different keys.  workaround is to always call the same fxn the same way
"""

class keyed_object(object):

    def get_key(self):
        raise NotImplementedError

class keyed_partial(partial, keyed_object):
    """
    will be created directly
    """
    def __init__(self, f, get_key_f, **kwargs):
        self.get_key_f = get_key_f
        partial.__init__(self, f, **kwargs)

    def get_key(self):
        assert self.args == ()
        return self.get_function_like_key(self.func, self.keywords)

default_keyed_partial = partial(keyed_partial, get_key_f=playground.default_get_function_like_key_f)

class keyed_func(object):
    """
    will usually be created via decorator
    """
    def __init__(self, f, get_key_f):
        self.f, self.get_key_f = f, get_key_f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def get_key(self):
        return self.get_key_f(self.f)

class keyed_func_dec(object):
    """
    decorator with arguments for creating keyed_func
    """
    def __init__(self, get_key_f):
        self.get_key_f = get_key_f

    def __call__(self, f):
        return keyed_func(f, self.get_key_f)

default_keyed_func_dec = partial(keyed_func_dec, get_key_f=playground.default_get_internal_key_f)
