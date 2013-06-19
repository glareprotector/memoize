import memoize
import dbs
import keyed_objects
import operator
import pdb
import functools
"""
test case: f1: applies input f to all elements of input list.  f2: partial that adds 2
"""

class asdf(object):

    def __init__(self, a, b):
        self.a, self.b = a,b

    def f(self):
        print self.a, self.b

    def __call__(self, x):
        print x


def g(a,*args,**kwargs):
    print a, args, kwargs

asdf2 = functools.partial(asdf,a=2,b=3)

gg = asdf(4,5)


it = asdf2()



"""
add_2_f = keyed_objects.keyed_partial(operator.add,2)

false_recalculate_determiner = lambda key, db: False
true_cache_determiner = lambda key,db: True
pickle_location_f = lambda key: ''

dbs = [dbs.pickle_db(pickle_location_f)]

memoized_map = memoize.memoizing_dec(dbs, false_recalculate_determiner, true_cache_determiner)(map)

memoized_map(add_2_f, [2,3,4])
pdb.set_trace()
memoized_map(add_2_f, [2,3,4])
pdb.set_trace()
"""
