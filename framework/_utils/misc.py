import os


def make_ext(name, ext):
    return '{}{}{}'.format(name, os.extsep, ext)


def datapath(*ps):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, '..', '..', 'data', *(str(p) for p in ps))


def flat_zip(*iterators):
    from operator import add
    from functools import reduce
    wrap = lambda obj: (obj,) if not isinstance(obj, tuple) else obj
    iterators = [iter(iterator) for iterator in iterators]
    while True:
        yield reduce(add, [wrap(next(iterator)) for iterator in iterators])
