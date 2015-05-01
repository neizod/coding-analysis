import os
import json
import logging
import statistics as stat
from collections import Counter, defaultdict

from framework._utils import datapath
from framework._utils import word_processor


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


def summary_row(answer):
    return '{} {} {} {}\n'.format(
            answer['pid'],
            answer['io'],
            answer['screen_name'],
            repr_or_na(answer['language']))


def calculate_identifier_length(year, **kwargs):
    os.makedirs(datapath('codejam', 'result'), exist_ok=True)
    with open(datapath('codejam', 'result', 'language.txt'), 'w') as file:
        file.write('pid io screen_name language\n')
        for answer in json.load(open(datapath('codejam', 'extract', 'language.json'))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('language', description='''
        This method will analyse language used in each subbmited code.''')
    # TODO force
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=calculate_identifier_length)