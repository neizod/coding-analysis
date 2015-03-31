import os
import sys
import yaml

basepath = os.path.dirname(__file__) + '/'

metadata = yaml.load(open(basepath + '../codejam/metadata.yaml'))
lang_name = yaml.load(open(basepath + '../codejam/lang_name.yaml'))

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
