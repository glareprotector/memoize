import memoize
import dbs
import keyed_objects
import operator
import pdb

"""
test case: f1: applies input f to all elements of input list.  f2: partial that adds 2
"""

add_2_f = keyed_objects.keyed_partial(operator.add,2)

false_recalculate_determiner = lambda key, db: False
true_cache_determiner = lambda key,db: True
dbs = [dbs.ram_db()]

memoized_map = memoize.memoizing_dec(dbs, false_recalculate_determiner, true_cache_determiner)(map)

memoized_map(add_2_f, [2,3,4])
pdb.set_trace()
memoized_map(add_2_f, [2,3,4])
pdb.set_trace()
