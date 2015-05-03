from framework._utils import hook_submodules


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    subparser.add_argument('year', type=int, choices=[2013, 2014],
            help='''year of a contest.''')
    hook_submodules(subparser, __file__, __name__)
