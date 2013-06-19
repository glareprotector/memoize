import os
import pickle
from functools import *
import pdb

class db(object):
    """
    abstract class
    assume db are just key to value mappings
    """

    def get(self, key):
        raise NotImplementedError

    def set(self, key, obj):
        raise NotImplementedError

    def clear(self, key):
        raise NotImplementedError

    def set_this_run(self, key):
        raise NotImplementedError

class ram_db(db):
    """
    nothing more than a dictionary
    """

    def __init__(self):
        self.d = {}
        self.setted = set()

    def get(self, key):
        print self.d
        return self.d[key]

    def set(self, key, obj):
        self.d[key] = obj
        self.setted.add(key)

    def set_this_run(self, key):
        return key in self.setted

    def clear(self, key):
        try:
            del self.d[key]
        except KeyError:
            pass


class file_db(db):
    """
    writer_f: given file and object, writes to the file
    reader_f: given file, returns the object
    get_file_location_f: given key, returns full file path
    """
    def __init__(self, get_file_location_f, printer_f, reader_f):
        self.get_file_location_f, self.printer_f, self.reader_f = get_file_location_f, printer_f, reader_f
        self.setted = set()

    def get(self, key):
        loc = self.get_file_location_f(key=key)
        folder = os.path.dirname(loc)
        if not os.path.exists(loc):
            raise KeyError
        else:
            if self.reader_f == None:
                raise NotImplementedError
            else:
                return self.reader_f(loc=loc)

    def set(self, key, obj):
        loc = self.get_file_location_f(key=key)
        folder = os.path.dirname(loc)
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.printer_f(loc=loc, obj=obj)
        self.setted.add(key)

    def set_this_run(self, key):
        return key in self.setted
    
    def clear(self, key):
        loc = self.get_file_location_f(key=key)
        try:
            os.remove(loc)
        except Exception:
            pass

def get_file_location_f(get_folder_f, get_name_f, key):
    return get_folder_f(key=key) + get_name_f(key=key)

def default_get_name_f(key):
    return str(key)

def default_get_folder_f(key):
    return 'dump/'

get_file_location_f_default_get_name = partial(get_file_location_f, get_name_f = default_get_name_f)

default_get_file_location_f = partial(get_file_location_f_default_get_name, get_folder_f=default_get_folder_f)

def pickle_printer_f(loc, obj):
    pickle.dump(obj, open(loc, 'wb'))

def pickle_reader_f(loc):
    return pickle.load(open(loc,'rb'))

pickle_db = partial(file_db, printer_f=pickle_printer_f, reader_f=pickle_reader_f)

a_pickle_db = partial(pickle_db, get_file_location_f=partial(get_file_location_f_default_get_name, get_folder_f=lambda key: './'))

default_pickle_db = partial(pickle_db, get_file_location_f=default_get_file_location_f)

def int_printer_f(loc, obj):
    f = open(loc, 'w')
    f.write(str(obj))
    f.close()

def int_reader_f(loc):
    f = open(loc, 'r')
    return int(f.next().strip())

int_db = partial(file_db, printer_f=int_printer_f, reader_f=int_reader_f)

default_int_db = partial(int_db, get_file_location_f=default_get_file_location_f)
