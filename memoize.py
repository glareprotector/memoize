
import dbs
import keyed_objects



class memoized_f(keyed_objects.keyed_object):
    """
    
    """

    def __init__(self, f, dbs, recalculate_determiner, cache_determiner):
        self.f, self.dbs, self.recalculate_determiner, self.cache_determiner = f, dbs, recalculate_determiner, cache_determiner

    def get_key(self):
        return get_internal_key(self, self.f)


    def get_cache_key(self, *args, **kwargs):
        """
        creates key that db uses to cache results.  key is a tuple, with an entry for each unnamed argument, and a (arg_name, arg_key) entry for each named argument
        """
        args_keys = map(self.get_internal_key, args)
        kwargs_keys = [(arg_name, self.get_internal_key(arg)) for arg_name, arg in kwargs.iteritems()]
        cache_key = tuple([self.get_internal_key(self.f)] + args_keys + kwargs_keys)
        return cache_key

    def __call__(self, *args, **kwargs):
        """
        recalculate_determiner gets to access the key and the db.  for example, it might need to get the date of an object.
        if recalculating, or all dbs fail, then compute the function
        """
        import pdb
        pdb.set_trace()
        cache_key = self.get_cache_key(*args, **kwargs)
        if not self.recalculate_determiner(cache_key, self.dbs):
            for db in self.dbs:
                try:
                    return db.get(cache_key)
                except KeyError, NotImplementedError:
                    pass

        obj = self.f(*args, **kwargs)
        for db in self.dbs:
            db.clear(cache_key)
            if self.cache_determiner(cache_key, db):
                db.set(cache_key, obj)
        return obj

class memoizing_dec(object):
    """
    enriches callable by generating function key, and feeding to db to cache
    returns a memoized_f object
    """
    def __init__(self, dbs, recalculate_determiner, cache_determiner):
        self.dbs, self.recalculate_determiner, self.cache_determiner = dbs, recalculate_determiner, cache_determiner

    def __call__(self, f):
        return memoized_f(f, self.dbs, self.recalculate_determiner, self.cache_determiner)
        
        
