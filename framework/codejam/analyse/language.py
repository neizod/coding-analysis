import os
import json

from framework._utils import datapath, hook_common_arguments


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


def summary_row(answer):
    return '{} {} {} {}\n'.format(
            answer['pid'],
            answer['io'],
            answer['screen_name'],
            repr_or_na(answer['language']))


def main(year, **_):
    os.makedirs(datapath('codejam', 'result'), exist_ok=True)
    with open(datapath('codejam', 'result', 'language-{}.txt'.format(year)), 'w') as file:
        file.write('pid io screen_name language\n')
        for answer in json.load(open(datapath('codejam', 'extract', 'language-{}.json'.format(year)))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('language', description='''
        This method will analyse language used in each subbmited code.''')
    hook_common_arguments(subparser, main)
