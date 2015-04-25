import os
import json

from ..._utils import datapath


def summary_row(answer):
    return '{} {}\n'.format(answer['pid'], len(answer['cheats']))


def calculate_cheat(year, **kwargs):
    os.makedirs(datapath('result'), exist_ok=True)
    with open(datapath('result', 'cheat.txt'), 'w') as file:
        file.write('pid nos-cheat\n')
        for answer in json.load(open(datapath('extract', 'cheat.json'))):
            file.write(summary_row(answer))


def update_parser(subparsers):
    subparser = subparsers.add_parser('cheat', description='''
        This method will analyse cheating by copy-paste source code
        from multiple contestants.''')
    subparser.add_argument('year', type=int, help='''
        year of a contest.''')
    # TODO force
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=calculate_cheat)
