import os
import sys
import builtins
import yaml

basepath = os.path.dirname(__file__) + '/'

metadata = yaml.load(open(basepath + 'metadata/main.yaml'))
lang_name = yaml.load(open(basepath + 'lang_name.yaml'))


def log(*sentences):
    print(*sentences, end='')
    sys.stdout.flush()


def makedirs(directory):
    return os.makedirs(basepath + directory, exist_ok=True)


def isfile(filename):
    return os.path.isfile(basepath + filename)


def open(filename, *args, **kwargs):
    return builtins.open(basepath + filename, *args, **kwargs)


def exist_source(attempt, submittime):
    if not attempt or submittime == -1:
        return False
    return True


def iter_id_io(problems):
    for problem in problems:
        c = 0
        while c < problem['io']:
            yield problem['id'], c
            c += 1
