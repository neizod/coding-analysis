from framework._utils import submodules


def update_parser(subparsers):
    subparser = subparsers.add_parser('extract')
    prepare_subparsers = subparser.add_subparsers()
    for module in submodules(__file__, __name__):
        module.update_parser(prepare_subparsers)
