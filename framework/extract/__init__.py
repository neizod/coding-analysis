from . import codejam


def update_parser(subparsers):
    subparser = subparsers.add_parser('extract')
    prepare_subparsers = subparser.add_subparsers()
    for module in [codejam]:
        module.update_parser(prepare_subparsers)
