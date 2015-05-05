from framework._utils import SubparsersHook
from framework.codejam._helper import available_years


class CodeJam(SubparsersHook):
    def modify_parser(self):
        self.parser.add_argument('-y', '--year', type=int, required=True,
                choices=available_years(), help='''year of a contest.''')
