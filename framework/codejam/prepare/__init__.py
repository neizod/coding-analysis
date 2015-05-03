from framework._utils import hook_submodules


def update_parser(subparsers):
    subparser = subparsers.add_parser('prepare')
    hook_submodules(subparser, __file__, __name__)
