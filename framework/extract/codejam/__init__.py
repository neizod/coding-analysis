from . import identifier


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    codejam_subparsers = subparser.add_subparsers()
    for module in [identifier]:
        module.update_parser(codejam_subparsers)
