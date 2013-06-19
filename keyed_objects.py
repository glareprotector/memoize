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

    def __init__(self, f, get_key_f):
        self.get_key_f = get_key_f
        partial.__init__(self, f, get_key_f)

    def get_key(self):
        assert self.args = []
        return self.get_function_like_key(self.func, self.keywords)

class keyed_func(object):

    def __init__(self, f, get_key_f):
        self.f, self.get_key_f = f, get_key_f

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    def get_key(self):
        return self.get_key_f(self.f)
