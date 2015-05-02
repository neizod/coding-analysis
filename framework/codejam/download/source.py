import os
import json
import urllib3
import logging
from itertools import count

from framework._utils import datapath
from framework.codejam._helper import api, iter_submission


def get_source(year, force=False, **kwargs):
    http = urllib3.PoolManager()
    default = {'cmd': 'GetSourceCode'}
    for cid, pid, io, screen_name in iter_submission(year):
        directory = datapath('codejam', 'sourcezip', pid, io)
        os.makedirs(directory, exist_ok=True)
        zippath = datapath(directory, screen_name+'.zip')
        if not force and os.path.isfile(zippath):
            logging.info('ignore: {} {} {}'.format(pid, io, screen_name))
            continue
        default['contest'] = cid
        default['problem'] = pid
        default['io_set_id'] = io
        default['username'] = screen_name
        logging.info('downloading: {} {} {}'.format(pid, io, screen_name))
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
