from . import codejam


def update_parser(subparsers):
    subparser = subparsers.add_parser('download')
    download_subparsers = subparser.add_subparsers()
    codejam.update_parser(download_subparsers)
