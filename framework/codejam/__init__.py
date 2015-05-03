from framework._utils import hook_submodules
from framework.codejam._helper import available_years


def update_parser(subparsers):
    subparser = subparsers.add_parser('codejam')
    subparser.add_argument('-y', '--year', type=int, required=True,
            choices=available_years(), help='''year of a contest.''')
    hook_submodules(subparser, __file__, __name__)
