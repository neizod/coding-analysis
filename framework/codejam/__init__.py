from framework._utils import submodules


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    subparser.add_argument('year', type=int, choices=[2013, 2014],
            help='''year of a contest.''')
    codejam_subparsers = subparser.add_subparsers()
    for module in submodules(__file__, __name__):
        module.update_parser(codejam_subparsers)
