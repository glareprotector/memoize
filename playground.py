        

def default_get_cache_key(self, get_internal_key_f, *args, **kwargs):
    """
    for use in memoized_f only
    creates key that db uses to cache results.  key is a tuple, with an entry for each unnamed argument, and a (arg_name, arg_key) entry for each named argument
    """
    args_keys = map(self.get_internal_key, args)
    kwargs_keys = [(arg_name, self.get_internal_key(arg)) for arg_name, arg in kwargs.iteritems()]
    cache_key = tuple([self.get_internal_key(self.f)] + args_keys + kwargs_keys)
    return cache_key

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


	
