import os
import pickle

class db(object):
    """
    object that stores objects.  decides how it wants to represent objects, since different db will have different ways.  eg, a dictionary can store objects, but a db that writes stuff to file can only store strings
    assume db are just key to value mappings
    """

    def get(self, key):
        raise NotImplementedError

    def get_obj_repr(self, obj):
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
    """
    def __init__(self, get_pickle_location_f):
        self.get_pickle_location_f = get_pickle_location_f

    def get_file_name(self, key):
        return self.get_pickle_location_f(key) + repr(key) + '.pickle'

    def get(self, key):
        loc = self.get_file_name(key)
        if not os.path.exists(loc):
            raise KeyError
        else:
            return pickle.load(open(loc,'rb'))

    def set(self, key, obj):
        loc = self.get_file_name(key)
        pickle.dump(obj, open(loc,'wb'))
    
    def clear(self, key):
        loc = self.get_file_name(key)
        try:
            os.remove(loc)
        except OSError:
            passz

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
