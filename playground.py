from functools import *

def default_get_internal_key(self, obj):
    """
    used by get_function_like_key to get representation of arguments and also itself
    interface: obj
    not keyed, not memoized
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

def get_function_like_key(get_internal_key_f, keys_to_ignore, f, **kwargs):
    """
    this is used by a fxn-like (includes regular fxns and partials) to decide how to key calls to itself.
    will be used as an argument when creating keyed_objects and keyed_partials(twice actually) 
    interface: f, **kwargs
    not keyed, not memoized
    """
    try:
        kwargs_keys = tuple(sorted([(arg_name, get_internal_key_f(arg)) for arg_name, arg in kwargs.iteritems() if arg_name not in keys_to_ignore], key = lambda x: x[0]))
    except AttributeError:
        kwargs_keys = ()

get_function_like_key_default_get_internal_key = partial(get_function_like_key, get_internal_key_f = default_get_internal_key)

default_get_function_like_key = partial(get_function_like_key_default_get_internal_key, keys_to_ignore = [])
