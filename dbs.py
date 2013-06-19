import os
import pickle

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

class ram_db(db):
    """
    nothing more than a dictionary
    """

    def __init__(self):
        self.d = {}

    def get(self, key):
        return self.d[key]

    def set(self, key, obj):
        self.d[key] = obj

    def clear(self, key):
        try:
            del self.d[key]
        except KeyError:
            pass


class pickle_db(db):
    """
    can handle any pickleable object
    get_pickle_file_location_f should take in a key, and output absolute location to store pickle
    """
    def __init__(self, get_pickle_file_location_f):
        self.get_pickle_file_location_f = get_pickle_file_location_f


    def get(self, key):
        loc = self.get_pickle_file_location(key)
        if not os.path.exists(loc):
            raise KeyError
        else:
            return pickle.load(open(loc,'rb'))

    def set(self, key, obj):
        loc = self.get_pickle_file_location(key)
        folder = os.path.dirname(loc)
        if not os.path.exists(folder):
            os.makedirs(folder)
        pickle.dump(obj, open(loc,'wb'))
    
    def clear(self, key):
        loc = self.get_pickle_file_location(key)
        try:
            os.remove(loc)
        except OSError:
            pass

class pretty_print_db(db):
    """
    only handles whatever pretty_printer and pretty_reader functions handle
    """
    def __init__(self, get_pickle_location_f, pretty_printer_f, pretty_reader_f):
        self.get_pickle_location_f, self.pretty_printer_f, self.pretty_reader_f = get_pickle_location_f, pretty_printer_f, pretty_reader_f

    def get_file_name(self, key):
        return self.get_pickle_location_f(key) + repr(key) + '.pretty'

    def get(self, key):
        loc = self.get_file_name(key)
        if not os.path.exists(loc):
            raise KeyError
        else:
            if self.pretty_reader_f == None:
                raise NotImplementedError
            else:
                return self.pretty_reader_f(loc)

    def set(self, key, obj):
        loc = self.get_file_name(key)
        f = open(loc, 'w')
        f.write(self.pretty_printer_f(obj))
    
    def clear(self, key):
        loc = self.get_file_name(key)
        os.remove(loc)
