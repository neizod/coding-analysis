from framework._utils import SubmodulesHook


class GitHub(SubmodulesHook):
    ''' This is main control for mining GitHub repositories. '''

    def modify_parser(self):
        self.parser.add_argument(
            '-l', '--only-lang', choices=['python', 'php'],
            help='''only this language.''')
