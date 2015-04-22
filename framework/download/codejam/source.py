import os
import json
import urllib3
from itertools import count

from ...utils import datapath, metadata, log, iter_id_io, exist_source


def prepare_dirs(year):
    os.makedirs(datapath('sourcezip'), exist_ok=True)
    for contest in metadata[year]:
        for problem in contest['problems']:
            pid = problem['id']
            for io in range(problem['io']):
                os.makedirs(datapath('sourcezip', pid, io), exist_ok=True)


def get_source(year, force=False, quiet=False, **kwargs):
    http = urllib3.PoolManager()
    api = metadata['api']
    default = {'cmd': 'GetSourceCode'}
    prepare_dirs(year)
    for contest in metadata[year]:
        filename = 'metadata/round/{}.json'.format(contest['id'])
        if not os.path.isfile(datapath(filename)):
            exit('data for year {} does not exist.'.format(year))
        default['contest'] = contest['id']
        for answer in json.load(open(datapath(filename))):
            name = answer['n']
            quiet or log(name)
            id_io = iter_id_io(contest['problems'])
            for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
                if not exist_source(a, s):
                    continue
                sourcezip = 'sourcezip/{}/{}/{}.zip'.format(num, io, answer['n'])
                if not force and os.path.isfile(datapath(sourcezip)):
                    quiet or log('_')
                    continue
                default['problem'] = num
                default['io_set_id'] = io
                default['username'] = name
                result = http.request('GET', api, fields=default)
                with open(datapath(sourcezip), 'wb') as file:
                    file.write(result.data)
                quiet or log('.')
            quiet or log('\n')


def update_parser(subparsers):
    subparser = subparsers.add_parser('source', description='''
        This script will download Google Code Jam submitted zipped sources.
        You need to run get_metadata script with supply argument of that year
        to build up list of contestants first.''')
    subparser.add_argument('year', type=int, help='''
        year of a contest to download sources.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force download source file if exists.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=get_source)
