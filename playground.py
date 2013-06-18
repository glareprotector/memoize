        

def default_get_cache_key(self, *args, **kwargs):
    """
    for use in memoized_f only
    creates key that db uses to cache results.  key is a tuple, with an entry for each unnamed argument, and a (arg_name, arg_key) entry for each named argument
    """
    args_keys = map(self.get_internal_key, args)
    kwargs_keys = [(arg_name, self.get_internal_key(arg)) for arg_name, arg in kwargs.iteritems()]
    cache_key = tuple([self.get_internal_key(self.f)] + args_keys + kwargs_keys)
    return cache_key


            


	
