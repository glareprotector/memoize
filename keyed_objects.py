import functools
import pdb

"""
separate get_key from memoized_f. memoized_f doesn't necessarily need to implement get_key, and a memoized_f doesn't necessarily need to implement get_key
how to create a keyed object?
- what if i have a keyed_partial, so that it implements get_key, and then i use it to create another keyed_partial.  what will the new get_key do?
  what does get_key store anyways?  it stores the information that affects output, outside of the arguments to the function.  so a partial should inherit that information
"""


class keyed_object(object):

    """
    this is used by 
    """
    def get_internal_key(self, obj):
        """
        takes in any object, and returns the internal key it will use for itself.
        """
        try:
            return obj.get_key()
        except AttributeError:
            pass
        try:
            return obj.__name__
        except AttributeError:
            pass
        try:
            return str(obj)
        except AttributeError:
            raise Exception

    def get_key(self):
        raise NotImplementedError

"""
both the regular keyed_object and keyed_partial need method that takes in an object and decides on its own internal representation of it.  for now, this will look first at the get_key function if the object has it
so here, basically, am specifying the get_key function for these keyed objects.  regular keyed_object gets key of the backing callable
how do i key a function? 1. new class that contains the function? 2, add get_key as an attribute
how do i decorate a callable (not via decorator notation?)? same options as above.  to get the key, can use the same function as above.  function is thus used to key own function and also key arguments to its own callable
how do i key a partial? can't use decorator notation.  regardless, do i use a new class? if not decoratoring, not necessarily working with premade copy of anything.
steps to memoize a partial.  wait, what if original function is already memoized? 
"""


class keyed_partial(functools.partial, keyed_object):

    def get_key(self):

        args_keys = map(self.get_internal_key, self.args)
        try:
            kwargs_keys = [(arg_name, self.get_internal_key(arg)) for arg_name, arg in self.keywords.iteritems()]
        except AttributeError:
            kwargs_keys = []
        key = tuple([self.get_internal_key(self.func)] + args_keys + kwargs_keys)
        return key

class keyed_func(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    def get_key(self):
        return self.f.__name__
