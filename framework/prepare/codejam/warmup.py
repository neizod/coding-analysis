import os

from ..._utils import datapath, iter_submission, log, readsource


def warmup_source(year, quiet=False, **kwargs):
    for pid, io, screen_name in iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        quiet or log(directory)
        for filename in os.listdir(datapath(directory)):
            if os.path.isfile(datapath(filename)):
                _ensure_readfile = len(readsource(datapath(directory, filename)))
        quiet or log('  done\n')


def update_parser(subparsers):
    subparser = subparsers.add_parser('warmup', description='''
        This method will warmup source code files for futher analysis.''')
    subparser.add_argument('year', type=int, help='''
        year of the contest.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run script quietly.''')
    subparser.set_defaults(function=warmup_source)
