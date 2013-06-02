import functools
import pdb

class keyed_object(object):

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

class keyed_partial(functools.partial, keyed_object):

    def get_key(self):
        pdb.set_trace()
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
