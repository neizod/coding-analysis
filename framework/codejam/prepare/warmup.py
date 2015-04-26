import os
import logging

from ..._utils import datapath, iter_submission, readsource


def warmup_source(year, **kwargs):
    for pid, io, screen_name in iter_submission(year):
        directory = datapath('source', pid, io, screen_name)
        logging.info('warming-up: {} {} {}'.format(pid, io, screen_name))
        for filename in os.listdir(directory):
            filepath = datapath(directory, filename)
            if os.path.isfile(filepath):
                _ensure_readfile = len(readsource(filepath))


def update_parser(subparsers):
    subparser = subparsers.add_parser('warmup', description='''
        This method will warmup source code files for futher analysis.''')
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=warmup_source)
