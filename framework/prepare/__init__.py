from . import codejam


def update_parser(subparsers):
    subparser = subparsers.add_parser('prepare')
    prepare_subparsers = subparser.add_subparsers()
    codejam.update_parser(prepare_subparsers)
