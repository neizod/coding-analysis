import json
import yaml
from itertools import repeat

from framework._utils import LazyLoader
from framework._utils.misc import datapath, make_ext, flat_zip


API = 'https://code.google.com/codejam/contest/scoreboard/do/'


class LazyMetadata(LazyLoader):
    ''' metadata for Google Code Jam. '''
    @staticmethod
    def load_data():
        return yaml.load(open(datapath('codejam', 'metadata', 'main.yaml')))


def readsource(filename):
    ''' returns file content within best known encoding used. '''
    try:
        return open(filename).read()
    except UnicodeDecodeError:
        return open(filename, encoding='latin1').read()


def iter_id_io(problems):
    ''' yields problem data along with io size. '''
    for problem in problems:
        yield from zip(repeat(problem['id']), range(problem['io']))


def iter_answer(problems, answer):
    ''' yields problem data zipped with answer data fron each contestant. '''
    yield from flat_zip(iter_id_io(problems), answer['att'], answer['ss'])


def iter_contest(year):
    ''' yields id of all contest in a year. '''
    with LazyMetadata() as metadata:
        yield from (contest['id'] for contest in metadata[year])


def iter_submission(year):
    ''' yields all submissions data of a year when data can have source. '''
    for cid, uname, pid, pio, attempt, submit_time in iter_all_attempt(year):
        if attempt and submit_time != -1:
            yield cid, pid, pio, uname


def iter_all_attempt(year):
    ''' yields all submissions data of a year. '''
    with LazyMetadata() as metadata:
        for contest in metadata[year]:
            filename = make_ext(contest['id'], 'json')
            filepath = datapath('codejam', 'metadata', 'round', filename)
            for answer in json.load(open(filepath)):
                yield from flat_zip(repeat(contest['id']),
                                    repeat(answer['n']),
                                    iter_answer(contest['problems'], answer))
