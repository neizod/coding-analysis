from . import codejam
from .codejam import metadata
from .codejam import source


def update_parser(subparsers):
    subparser = subparsers.add_parser('download')
    download_subparsers = subparser.add_subparsers()
    codejam.metadata.update_parser(download_subparsers)
    codejam.source.update_parser(download_subparsers)
