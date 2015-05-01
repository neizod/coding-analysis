import json
import yaml

from framework._utils import datapath, make_ext


def readsource(filename):
    try:
        return open(filename).read()
    except UnicodeDecodeError:
        return open(filename, encoding='latin1').read()


def exist_source(attempt, submittime):
    return attempt and submittime != -1


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
        file_ext = make_ext(contest['id'], 'json')
        filepath = datapath('codejam', 'metadata', 'round', file_ext)
        for answer_set in json.load(open(filepath)):
            screen_name = answer_set['n']
            for pid, io, a, s in iter_answer(contest['problems'], answer_set):
                if exist_source(a, s):
                    yield pid, io, screen_name


metadata = yaml.load(open(datapath('codejam', 'metadata', 'main.yaml')))
