from . import metadata
from . import source


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    codejam_subparsers = subparser.add_subparsers()
    metadata.update_parser(codejam_subparsers)
    source.update_parser(codejam_subparsers)
