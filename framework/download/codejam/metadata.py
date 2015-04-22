import os
import json
import urllib3
from itertools import count

from ...utils import datapath, metadata, log


def get_metadata(year, force=False, quiet=False, **kwargs):
    http = urllib3.PoolManager()
    api = metadata['api']
    default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
    os.makedirs(datapath('metadata/round'), exist_ok=True)
    for contest in metadata[year]:
        filename = 'metadata/round/{}.json'.format(contest['id'])
        if not force and os.path.isfile(datapath(filename)):
            continue
        quiet or log(contest['id'])
        default['contest_id'] = contest['id']
        contest_stat = []
        for i in count(1, 30):
            default['start_pos'] = i
            result = http.request('GET', api, fields=default)
            data = json.loads(result.data.decode('utf-8'))
            contest_stat += data['rows']
            quiet or log('.')
            if i + 30 > data['stat']['nrp']:
                break
        with open(datapath(filename), 'w') as file:
            json.dump(contest_stat, file, sort_keys=True, indent=4)
        quiet or log('\n')


def update_parser(subparsers):
    subparser = subparsers.add_parser('metadata', description='''
        This script will download Google Code Jam each round metadata
        of a suppliment year, and store each as JSON file.''')
    subparser.add_argument('year', type=int, help='''
        year of a contest to download sources.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force download metadata file if exists.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=get_metadata)
