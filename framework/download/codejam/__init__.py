from . import metadata
from . import source


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    codejam_subparsers = subparser.add_subparsers()
    for module in [metadata, source]:
        module.update_parser(codejam_subparsers)
