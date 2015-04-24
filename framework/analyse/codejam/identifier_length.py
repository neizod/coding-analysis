import os
import json
import statistics as stat

from ..._utils import datapath
from ..._utils import word_processor


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


def summary_row(answer):
    if not answer['identifiers']:
        mean = None
    else:
        mean = stat.mean(len(iden) for iden in answer['identifiers'])
    return '{} {} {} {}\n'.format(
            answer['pid'],
            answer['io'],
            answer['screen_name'],
            repr_or_na(mean))


def calculate_identifier_length(year, **kwargs):
    os.makedirs(datapath('result'), exist_ok=True)
    with open(datapath('result', 'identifier-length.txt'), 'w') as file:
        file.write('pid io screen_name identifier-length\n')
        for answer in json.load(open(datapath('extract', 'identifier.json'))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('identifier-length', description='''
        This method will analyse identifier length from extracted data
        of submitted Google Code Jam source code.''')
    subparser.add_argument('year', type=int, help='''
        year of a contest.''')
    # TODO force
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=calculate_identifier_length)
