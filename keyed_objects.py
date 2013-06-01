import functools

class keyed_object(object):

    def get_internal_key(self, obj):
        """
        takes in any object, and returns the internal key it will use for itself.
        """
        try:
            return obj.get_key()
        except:
            return obj.__hash__()

    def get_key(self):
        raise NotImplementedError

class keyed_partial(functools.partial):

    def get_key(self):
        args_keys = map(self.get_object_key, *args)
        kwargs_keys = [(arg_name, self.get_object_key(arg)) for arg_name, arg in **kwargs.iteritems()]
        key = tuple([self.get_interval_key(self.func) + ]args_keys + kwargs_keys)
        return key

class keyed_func(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    def get_key(self):
        return self.f.__name__
