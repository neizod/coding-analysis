import os
import json
import logging

from ..._utils import datapath
from ..._utils import word_processor
from ..._utils.word_processor import Identifier


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


def summary_row(answer):
    if not answer['identifiers']:
        mean = None
    else:
        mean = sum(Identifier.is_readable(iden) for iden in answer['identifiers']) / len(answer['identifiers'])
    return '{} {} {} {}\n'.format(
            answer['pid'],
            answer['io'],
            answer['screen_name'],
            repr_or_na(mean))


def calculate_identifier_readable(year, **kwargs):
    os.makedirs(datapath('result'), exist_ok=True)
    with open(datapath('result', 'identifier-readable.txt'), 'w') as file:
        file.write('pid io screen_name identifier-readable\n')
        for answer in json.load(open(datapath('extract', 'identifier.json'))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('identifier-readable', description='''
        This method will analyse identifier readable from extracted data
        of submitted Google Code Jam source code.''')
    # TODO force
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=calculate_identifier_readable)
