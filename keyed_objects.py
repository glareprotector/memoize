import functools
import pdb
import playground

"""
keyed_objects only need to implement get_key.  
convention: will only call function using keyworded arguments
note: not using functional programming for these objects.  instead, am binding get_key functions to each class of keyed_objects
key will consist of 
"""

class keyed_object(object):

    def get_key(self):
        raise NotImplementedError

class keyed_partial(functools.partial, keyed_object):

    def get_key(self):
        """
        unfortunately, partial function call does not have same key as full function call with same parameters
        however, partials ultimately end up calling the base function, and if that is memoized, there's no need
        """
        assert self.args == []
        try:
            kwargs_keys = tuple(sorted([(arg_name, playground.get_internal_key(arg)) for arg_name, arg in self.keywords.iteritems()], key = lambda x: x[0]))
        except AttributeError:
            kwargs_keys = ()
        key = tuple(playground.get_internal_key(self.func), kwargs_keys)
        return key

class keyed_func(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    def get_key(self):
        return self.f.__name__
