import os
import logging
from zipfile import ZipFile, BadZipFile

from ..._utils import datapath, iter_submission


def ensure_recursive_unzip(year):
    for pid, io, screen_name in utils.iter_submission(year):
        directory = datapath('source', pid, io, screen_name)
        for filename in os.listdir(directory):
            filepath = datapath(directory, filename)
            if os.path.splitext(filepath)[1] == '.zip':
                with ZipFile(filepath) as z:
                    z.extractall(directory)
                os.remove(filepath)


def unzip_source(year, force=False, **kwargs):
    bad_zipfiles = []
    for pid, io, screen_name in iter_submission(year):
        zippath = datapath('sourcezip', pid, io, screen_name+'.zip')
        directory = datapath('source', pid, io, screen_name)
        os.makedirs(directory, exist_ok=True)
        logging.info('unzipping: {} {} {}'.format(pid, io, screen_name))
        if force or not os.listdir(directory):
            try:
                with ZipFile(zippath) as z:
                    z.extractall(directory)
            except BadZipFile:
                bad_zipfiles += [zippath]
    if bad_zipfiles:
        for zippath in bad_zipfiles:
            os.renames(zippath, datapath('badzip', zippath))
        raise BadZipFile(bad_zipfiles)
    ensure_recursive_unzip(year)


def update_parser(subparsers):
    subparser = subparsers.add_parser('unzip', description='''
        This method will unzip downloaded source code files.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force unzip source code files if destination exists.''')
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=unzip_source)
