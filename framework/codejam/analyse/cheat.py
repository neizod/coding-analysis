import os
import json
import logging

from ..._utils import datapath


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
    # TODO force
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=calculate_cheat)
