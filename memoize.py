 
import dbs
import keyed_objects
import pdb


class memoized_f(keyed_objects.keyed_object):

    def __init__(self, f, dbs, recalculate_determiner_f, get_cache_key_f):
        self.f, self.dbs, self.recalculate_determiner_f, self.get_cache_key_f = f, dbs, recalculate_determiner_f, get_cache_key_f

    def get_key(self):
        return self.f.get_key()


    def __call__(self, *args, **kwargs):
        """
        if item is recalculated, it should be updated in all dbs
        if item is retrieved, it should be updated in all dbs.
        may add more flexibility later, including telling db not to update same key more than once, since in same program run, code is the same, so computed value should be the same
        """
        assert args == ()
        cache_key = self.get_cache_key_f(f=self.f, keywords=kwargs)

        found_cached = False

        for db in self.dbs:
            if db.set_this_run(cache_key) or not self.recalculate_determiner_f(cache_key, self.dbs):
                try:
                    obj = db.get(cache_key)
                except KeyError, NotImplementedError:
                    pass
                else:
                    found_cached = True

        if not found_cached:
            obj = self.f(**kwargs)
        for db in self.dbs:
            db.clear(cache_key)
            db.set(cache_key, obj)
        return obj

class memoizing_dec(object):
    """
    enriches callable by generating function key, and feeding to db to cache
    returns a memoized_f object
    """
    def __init__(self, dbs, recalculate_determiner_f, get_cache_key_f):
        self.dbs, self.recalculate_determiner_f, self.get_cache_key_f = dbs, recalculate_determiner_f, get_cache_key_f

    def __call__(self, f):
        return memoized_f(f, self.dbs, self.recalculate_determiner_f, self.get_cache_key_f)
        
        
