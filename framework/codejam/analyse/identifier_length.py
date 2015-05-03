import os
import json
import logging
import statistics as stat

from framework._utils import datapath, hook_common_arguments
from framework._utils import word_processor


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


def main(year, **kwargs):
    os.makedirs(datapath('codejam', 'result'), exist_ok=True)
    with open(datapath('codejam', 'result', 'identifier-length-{}.txt'.format(year)), 'w') as file:
        file.write('pid io screen_name identifier-length\n')
        for answer in json.load(open(datapath('codejam', 'extract', 'identifier-{}.json'.format(year)))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('identifier-length', description='''
        This method will analyse identifier length from extracted data
        of submitted Google Code Jam source code.''')
    hook_common_arguments(subparser, main)
