import os
import json
import urllib3
import logging
from itertools import count

from ..._utils import datapath, metadata


def get_metadata(year, force=False, **kwargs):
    http = urllib3.PoolManager()
    api = metadata['api']
    default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
    os.makedirs(datapath('metadata', 'round'), exist_ok=True)
    for contest in metadata[year]:
        filepath = datapath('metadata', 'round', str(contest['id'])+'.json')
        if not force and os.path.isfile(filepath):
            continue
        default['contest_id'] = contest['id']
        contest_stat = []
        for i in count(1, 30):
            default['start_pos'] = i
            result = http.request('GET', api, fields=default)
            data = json.loads(result.data.decode('utf-8'))
            contest_stat += data['rows']
            logging.info('downloading: {} {}'.format(contest['id'], i))
            if i + 30 > data['stat']['nrp']:
                break
        with open(filepath, 'w') as file:
            json.dump(contest_stat, file, sort_keys=True, indent=4)


def update_parser(subparsers):
    subparser = subparsers.add_parser('metadata', description='''
        This script will download Google Code Jam each round metadata
        of a suppliment year, and store each as JSON file.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force download metadata file if exists.''')
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=get_metadata)
