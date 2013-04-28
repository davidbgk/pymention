import pickle

relations_filename = 'relations.pkl'
targets_filename = 'targets.pkl'


def store_relation(source, target):
    """Stores a relation in the dedicated pickled file."""
    with open(relations_filename, 'wb') as relations_file:
        data = pickle.load(relations_file)
        data[source] = target
        pickle.dump(data, relations_file)


def retrieve_relation(source=None, target=None):
    """Retrieves a relation from its source and/or target."""
    with open(relations_filename, 'rb') as relations_file:
        data = pickle.load(relations_file)
        if target is None:
            return source, data[source]
        elif source is None:
            for k, v in data.iteritems():
                if v == target:
                    return k, v
        else:
            if data[source] == target:
                return source, target
            else:
                return None


def is_valid_target(target):
    """Checks the existence of an URI in the dedicated pickled file."""
    with open(targets_filename, 'rb') as targets_file:
        data = pickle.load(targets_file)
        for k, v in data.iteritems():
            if v == target:
                return True
        return False
