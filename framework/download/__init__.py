from .. import codejam
from ..codejam import get_metadata
from ..codejam import get_source


def update_parser(subparsers):
    subparser = subparsers.add_parser('download')
    download_subparsers = subparser.add_subparsers()
    codejam.get_metadata.update_parser(download_subparsers)
    codejam.get_source.update_parser(download_subparsers)
