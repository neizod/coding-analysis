import os
import json
import urllib3
import logging
from itertools import count

from framework._utils import datapath, hook_common_arguments
from framework.codejam._helper import api, iter_contest


def main(year, force=False, **kwargs):
    http = urllib3.PoolManager()
    default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
    os.makedirs(datapath('codejam', 'metadata', 'round'), exist_ok=True)
    for cid in iter_contest(year):
        filepath = datapath('codejam', 'metadata', 'round', str(cid)+'.json')
        if not force and os.path.isfile(filepath):
            continue
        default['contest_id'] = cid
        contest_stat = []
        for i in count(1, 30):
            default['start_pos'] = i
            result = http.request('GET', api, fields=default)
            data = json.loads(result.data.decode('utf-8'))
            contest_stat += data['rows']
            logging.info('downloading: {} {}'.format(cid, i))
            if i + 30 > data['stat']['nrp']:
                break
        with open(filepath, 'w') as file:
            json.dump(contest_stat, file, sort_keys=True, indent=4)


def update_parser(subparsers):
    subparser = subparsers.add_parser('metadata', description='''
        This script will download Google Code Jam each round metadata
        of a suppliment year, and store each as JSON file.''')
    hook_common_arguments(subparser, main)
