import os
import json
import urllib3
import logging
from itertools import count

from ..._utils import datapath, metadata, iter_id_io, exist_source


def prepare_dirs(year):
    os.makedirs(datapath('codejam', 'sourcezip'), exist_ok=True)
    for contest in metadata[year]:
        for problem in contest['problems']:
            pid = problem['id']
            for io in range(problem['io']):
                os.makedirs(datapath('codejam', 'sourcezip', pid, io), exist_ok=True)


def get_source(year, force=False, **kwargs):
    http = urllib3.PoolManager()
    api = metadata['api']
    default = {'cmd': 'GetSourceCode'}
    prepare_dirs(year)
    for contest in metadata[year]:
        filepath = datapath('codejam', 'metadata', 'round', str(contest['id'])+'.json')
        if not os.path.isfile(filepath):
            exit('data for year {} does not exist.'.format(year))
        default['contest'] = contest['id']
        for answer in json.load(open(filepath)):
            name = answer['n']
            id_io = iter_id_io(contest['problems'])
            for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
                if not exist_source(a, s):
                    continue
                zippath = datapath('codejam', 'sourcezip', num, io, name+'.zip')
                if not force and os.path.isfile(zippath):
                    logging.info('ignore: {} {} {}'.format(num, io, name))
                    continue
                logging.info('downloading: {} {} {}'.format(num, io, name))
                default['problem'] = num
                default['io_set_id'] = io
                default['username'] = name
                result = http.request('GET', api, fields=default)
                with open(zippath, 'wb') as file:
                    file.write(result.data)


def update_parser(subparsers):
    subparser = subparsers.add_parser('source', description='''
        This script will download Google Code Jam submitted zipped sources.
        You need to run get_metadata script with supply argument of that year
        to build up list of contestants first.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force download source file if exists.''')
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=get_source)
