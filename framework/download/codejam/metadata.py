import json
import urllib3
from itertools import count

from ... import utils


def get_metadata(year, force=False, quiet=False, **kwargs):
    http = urllib3.PoolManager()
    api = utils.metadata['api']
    default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
    utils.makedirs('metadata/round')
    for contest in utils.metadata[year]:
        filename = 'metadata/round/{}.json'.format(contest['id'])
        if not force and utils.isfile(filename):
            continue
        quiet or utils.log(contest['id'])
        default['contest_id'] = contest['id']
        contest_stat = []
        for i in count(1, 30):
            default['start_pos'] = i
            result = http.request('GET', api, fields=default)
            data = json.loads(result.data.decode('utf-8'))
            contest_stat += data['rows']
            quiet or utils.log('.')
            if i + 30 > data['stat']['nrp']:
                break
        with utils.open(filename, 'w') as file:
            json.dump(contest_stat, file, sort_keys=True, indent=4)
        quiet or utils.log('\n')


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
