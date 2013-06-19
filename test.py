import memoize
import dbs
import keyed_objects
import operator
import pdb
import functools
import playground
"""
test case: f1: applies input f to all elements of input list.  f2: partial that adds 2
"""

true_recalculate_determiner_f = lambda key, dbs: True
false_recalculate_determiner_f = lambda key, dbs: False

@memoize.memoizing_dec(dbs=[dbs.ram_db(),dbs.default_int_db()], recalculate_determiner_f=false_recalculate_determiner_f, get_cache_key_f = playground.default_get_function_like_key_f)
@keyed_objects.default_keyed_func_dec()
def fxn(x):
    print x
    if x <= 0:
        return x
    else:
        return fxn(x=x-1) + 1

print fxn(x=10)
print fxn(x=14)


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
