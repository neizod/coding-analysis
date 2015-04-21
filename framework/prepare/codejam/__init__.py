from . import unzip
from . import warmup


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    codejam_subparsers = subparser.add_subparsers()
    for module in [unzip, warmup]:
        module.update_parser(codejam_subparsers)
