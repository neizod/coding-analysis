import os
import logging
from zipfile import ZipFile, BadZipFile

from framework._utils import datapath, hook_common_arguments
from framework.codejam._helper import iter_submission


def ensure_recursive_unzip(year):
    for _, pid, io, screen_name in utils.iter_submission(year):
        directory = datapath('codejam', 'source', pid, io, screen_name)
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if os.path.splitext(filepath)[1] == '.zip':
                with ZipFile(filepath) as z:
                    z.extractall(directory)
                os.remove(filepath)


def main(year, force=False, **kwargs):
    bad_zipfiles = []
    for _, pid, io, screen_name in iter_submission(year):
        zippath = datapath('codejam', 'sourcezip', pid, io, screen_name+'.zip')
        directory = datapath('codejam', 'source', pid, io, screen_name)
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
            os.renames(zippath, datapath('codejam', 'badzip', zippath))
        raise BadZipFile(bad_zipfiles)
    ensure_recursive_unzip(year)


def update_parser(subparsers):
    subparser = subparsers.add_parser('unzip', description='''
        This method will unzip downloaded source code files.''')
    hook_common_arguments(subparser, main)
