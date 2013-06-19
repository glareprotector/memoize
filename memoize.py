 
import dbs
import keyed_objects
import pdb


class memoized_f(keyed_objects.keyed_object):
    """
    stuff in init does not affect the actual thing computed
    can memoize partials too??
    although i had hoped that i could code a memoized_f without caring about whether or not the object was keyed, since the decorator returns a new object, and i want new object to have a get_key if original object had it,
    i have to implement a get_key that simply calls original object's get_key.
    """

    def __init__(self, f, dbs, recalculate_determiner, cache_determiner, get_cache_key_f):
        self.f, self.dbs, self.recalculate_determiner, self.cache_determiner = f, dbs, recalculate_determiner, cache_determiner, get_cache_key_f

    def get_key(self):
        """
        behavior when calling get_key is exact the same as if calling self.f's get_key.  for example, if self.f doesn't have get_key, then AttributeError will be raised in both cases.
        only thing that differs is that it is not the direct get_key that raises the Error.
        """
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
    def __init__(self, dbs, recalculate_determiner, cache_determiner):
        self.dbs, self.recalculate_determiner, self.cache_determiner = dbs, recalculate_determiner, cache_determiner

    def __call__(self, f):
        return memoized_f(f, self.dbs, self.recalculate_determiner, self.cache_determiner)
        
        
