import os
from zipfile import ZipFile, BadZipFile

from ...utils import datapath, iter_submission, log


def ensure_recursive_unzip(year):
    for pid, io, screen_name in utils.iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        for filename in os.listdir(datapath(directory)):
            if os.path.splitext(datapath(filename))[1] == '.zip':
                with ZipFile(datapath(directory, filename)) as z:
                    z.extractall(datapath(directory))
                os.remove(datapath(directory, filename))



def unzip_source(year, force=False, quiet=False, **kwargs):
    bad_zipfiles = []
    for pid, io, screen_name in iter_submission(year):
        zipfiles = 'sourcezip/{}/{}/{}.zip'.format(pid, io, screen_name)
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        os.makedirs(datapath(directory), exist_ok=True)
        quiet or log(directory)
        if force or not os.listdir(datapath(directory)):
            quiet or log(' unzipped\n')
            try:
                with ZipFile(datapath(zipfiles)) as z:
                    z.extractall(datapath(directory))
            except BadZipFile:
                bad_zipfiles += [zipfiles]
        else:
            quiet or log(' exists\n')
    if bad_zipfiles:
        for zipfile in bad_zipfiles:
            os.renames(datapath(zipfile), datapath('badzip', zipfile))
        raise BadZipFile(bad_zipfiles)
    ensure_recursive_unzip(year)


def update_parser(subparsers):
    subparser = subparsers.add_parser('unzip', description='''
        This method will unzip downloaded source code files.''')
    subparser.add_argument('year', type=int, help='''
        year of contest to unzip source code files.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force unzip source code files if destination exists.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=unzip_source)
