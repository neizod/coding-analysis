import os
import logging

from framework._utils import datapath, hook_common_arguments
from framework.codejam._helper import readsource, iter_submission


def main(year, **_):
    for _, pid, io, screen_name in iter_submission(year):
        wc = 0
        directory = datapath('codejam', 'source', pid, io, screen_name)
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if os.path.isfile(filepath):
                wc += len(readsource(filepath))
        logging.info('warm-up: {} {} {} {}'.format(pid, io, screen_name, wc))


def update_parser(subparsers):
    subparser = subparsers.add_parser('warmup', description='''
        This method will warmup source code files for futher analysis.''')
    hook_common_arguments(subparser, main)
