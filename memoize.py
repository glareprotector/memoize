 
import dbs
import keyed_objects
import pdb


class memoized_f(keyed_objects.keyed_object):

    def __init__(self, f, dbs, recalculate_determiner, cache_determiner, get_cache_key_f):
        self.f, self.dbs, self.recalculate_determiner, self.cache_determiner, self.get_cache_key = f, dbs, recalculate_determiner, cache_determiner, get_cache_key_f

    def get_key(self):
        return self.f.get_key()


    def __call__(self, *args, **kwargs):
        """
        recalculate_determiner gets to access the key and the db.  for example, it might need to get the date of an object.
        if recalculating, or all dbs fail, then compute the function
        """
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
    def __init__(self, dbs, recalculate_determiner, cache_determiner, get_cache_key_f):
        self.dbs, self.recalculate_determiner, self.cache_determiner, self.get_cache_key_f = dbs, recalculate_determiner, cache_determiner, get_cache_key_f

    def __call__(self, f):
        return memoized_f(f, self.dbs, self.recalculate_determiner, self.cache_determiner)
        
        
