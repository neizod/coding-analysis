import os
import json
import logging

from framework._utils import datapath, hook_common_arguments


def summary_row(answer):
    return '{} {}\n'.format(answer['pid'], len(answer['cheats']))


def calculate_cheat(year, **kwargs):
    os.makedirs(datapath('codejam', 'result'), exist_ok=True)
    with open(datapath('codejam', 'result', 'cheat.txt'), 'w') as file:
        file.write('pid nos-cheat\n')
        for answer in json.load(open(datapath('codejam', 'extract', 'cheat.json'))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('cheat', description='''
        This method will analyse cheating by copy-paste source code
        from multiple contestants.''')
    subparser.set_defaults(function=calculate_cheat)
    hook_common_arguments(subparser)
