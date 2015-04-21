from . import unzip


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    codejam_subparsers = subparser.add_subparsers()
    unzip.update_parser(codejam_subparsers)
