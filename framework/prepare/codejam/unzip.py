from zipfile import ZipFile, BadZipFile

from ... import utils as dry


def ensure_recursive_unzip(year):
    for pid, io, screen_name in dry.iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        for filename in dry.listdir(directory):
            if dry.splitext(filename)[1] == '.zip':
                with ZipFile(dry.datapath + directory + filename) as z:
                    z.extractall(dry.datapath + directory)
                dry.remove(directory + filename)



def unzip_source(year, force=False, quiet=False, **kwargs):
    bad_zipfiles = []
    for pid, io, screen_name in dry.iter_submission(year):
        zipfiles = 'sourcezip/{}/{}/{}.zip'.format(pid, io, screen_name)
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        dry.makedirs(directory)
        quiet or dry.log(directory)
        if force or not dry.listdir(directory):
            quiet or dry.log(' unzipped\n')
            try:
                with ZipFile(dry.datapath + zipfiles) as z:
                    z.extractall(dry.datapath + directory)
            except BadZipFile:
                bad_zipfiles += [zipfiles]
        else:
            quiet or dry.log(' exists\n')
    if bad_zipfiles:
        for zipfile in bad_zipfiles:
            dry.renames(zipfile, 'badzip/' + zipfile)
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
