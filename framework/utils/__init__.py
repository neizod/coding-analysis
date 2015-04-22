import os
import sys
import json
import yaml

basepath = os.path.dirname(__file__) + '/'
datapath = basepath + '../../data/codejam/'

metadata = yaml.load(open(datapath + 'metadata/main.yaml'))
lang_name = yaml.load(open(datapath + 'lang_name.yaml'))


def datapath(*path):
    return os.path.join(datapath, *path)


def log(*sentences):
    print(*sentences, end='')
    sys.stdout.flush()


def readsource(filename):
    try:
        return open(filename).read()
    except UnicodeDecodeError:
        return open(filename, encoding='latin1').read()


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


def iter_answer(problems, answer_set):
    it_problems = iter_id_io(problems)
    it_answer = zip(answer_set['att'], answer_set['ss'])
    for _ in answer_set:
        pid, io = next(it_problems)
        att, stime = next(it_answer)
        yield pid, io, att, stime


def iter_submission(year):
    for contest in metadata[year]:
        filename = 'metadata/round/{}.json'.format(contest['id'])
        for answer_set in json.load(open(datapath(filename))):
            screen_name = answer_set['n']
            for pid, io, a, s in iter_answer(contest['problems'], answer_set):
                if exist_source(a, s):
                    yield pid, io, screen_name
