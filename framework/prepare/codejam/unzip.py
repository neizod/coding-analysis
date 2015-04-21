from zipfile import ZipFile, BadZipFile

from ... import utils as dry


def unzip_source(year, force=False, quiet=False, **kwargs):
    bad_zipfiles = []
    for pid, io, screen_name in dry.iter_submission(year):
        zipfiles = 'sourcezip/{}/{}/{}.zip'.format(pid, io, screen_name)
        destination = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        dry.makedirs(destination)
        quiet or dry.log(destination)
        if force or not dry.listdir(destination):
            quiet or dry.log(' unzipped\n')
            try:
                with ZipFile(dry.datapath + zipfiles) as z:
                    z.extractall(dry.datapath + destination)
            except BadZipFile:
                bad_zipfiles += [zipfiles]
        else:
            quiet or dry.log(' exists\n')
    if bad_zipfiles:
        for zipfile in bad_zipfiles:
            dry.renames(zipfile, 'badzip/' + zipfile)
        raise BadZipFile(bad_zipfiles)


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
