import json
import yaml
from itertools import repeat

from framework._utils import LazyLoader, datapath, make_ext, flat_zip


API = 'https://code.google.com/codejam/contest/scoreboard/do/'


class LazyMetadata(LazyLoader):
    @staticmethod
    def load_data():
        return yaml.load(open(datapath('codejam', 'metadata', 'main.yaml')))


def readsource(filename):
    try:
        return open(filename).read()
    except UnicodeDecodeError:
        return open(filename, encoding='latin1').read()


def exist_source(attempt, submit_time):
    return attempt and submit_time != -1


def iter_id_io(problems):
    for problem in problems:
        yield from zip(repeat(problem['id']), range(problem['io']))


def iter_answer(problems, answer):
    yield from flat_zip(iter_id_io(problems), answer['att'], answer['ss'])


def iter_contest(year):
    with LazyMetadata() as metadata:
        yield from (contest['id'] for contest in metadata[year])


def iter_submission(year):
    for cid, uname, pid, pio, attempt, submit_time in iter_all_attempt(year):
        if exist_source(attempt, submit_time):
            yield cid, pid, pio, uname


def iter_all_attempt(year):
    with LazyMetadata() as metadata:
        for contest in metadata[year]:
            filename = make_ext(contest['id'], 'json')
            filepath = datapath('codejam', 'metadata', 'round', filename)
            for answer in json.load(open(filepath)):
                yield from flat_zip(repeat(contest['id']),
                                    repeat(answer['n']),
                                    iter_answer(contest['problems'], answer))
