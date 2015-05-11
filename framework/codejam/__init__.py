from framework._utils import SubmodulesHook


class CodeJam(SubmodulesHook):
    ''' This is main control for mining Google Code Jam data. '''

    def modify_parser(self):
        self.parser.add_argument(
            '-y', '--year', type=int, required=True,
            choices=[2012, 2013, 2014], help='''year of a contest.''')
