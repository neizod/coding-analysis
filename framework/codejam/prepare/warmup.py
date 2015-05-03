import os
import logging

from framework._utils import datapath, hook_common_arguments
from framework.codejam._helper import readsource, iter_submission


def warmup_source(year, **kwargs):
    for _, pid, io, screen_name in iter_submission(year):
        directory = datapath('codejam', 'source', pid, io, screen_name)
        logging.info('warming-up: {} {} {}'.format(pid, io, screen_name))
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if os.path.isfile(filepath):
                _ensure_readfile = len(readsource(filepath))


def update_parser(subparsers):
    subparser = subparsers.add_parser('warmup', description='''
        This method will warmup source code files for futher analysis.''')
    subparser.set_defaults(function=warmup_source)
    hook_common_arguments(subparser)
