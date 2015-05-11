import os


def make_ext(*name_parts):
    return os.extsep.join(str(part) for part in name_parts)


def datapath(*paths):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..', '..', 'data',
                                        *(str(path) for path in paths)))


def flat_zip(*iterators):
    from operator import add
    from functools import reduce
    wrap = lambda obj: (obj,) if not isinstance(obj, tuple) else obj
    iterators = [iter(iterator) for iterator in iterators]
    while True:
        yield reduce(add, [wrap(next(iterator)) for iterator in iterators])
