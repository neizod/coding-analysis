import os
from zipfile import ZipFile, BadZipFile

from ... import utils


def ensure_recursive_unzip(year):
    for pid, io, screen_name in utils.iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        for filename in os.listdir(utils.data(directory)):
            if os.path.splitext(utils.data(filename))[1] == '.zip':
                with ZipFile(utils.data(directory, filename)) as z:
                    z.extractall(utils.data(directory))
                os.remove(utils.data(directory, filename))



def unzip_source(year, force=False, quiet=False, **kwargs):
    bad_zipfiles = []
    for pid, io, screen_name in utils.iter_submission(year):
        zipfiles = 'sourcezip/{}/{}/{}.zip'.format(pid, io, screen_name)
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        os.makedirs(utils.data(directory), exist_ok=True)
        quiet or utils.log(directory)
        if force or not os.listdir(utils.data(directory)):
            quiet or utils.log(' unzipped\n')
            try:
                with ZipFile(utils.data(zipfiles)) as z:
                    z.extractall(utils.data(directory))
            except BadZipFile:
                bad_zipfiles += [zipfiles]
        else:
            quiet or utils.log(' exists\n')
    if bad_zipfiles:
        for zipfile in bad_zipfiles:
            os.renames(utils.data(zipfile), utils.data('badzip', zipfile))
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
