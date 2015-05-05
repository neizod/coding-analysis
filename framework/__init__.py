import logging

from framework._utils import SubparsersHook


class MainParser(SubparsersHook):
    def main(self):
        args = self.parser.parse_args()
        if 'function' in args:
            logging.basicConfig(level=args.quiet)
            args.function(**vars(args))
        else:
            import sys
            self.parser.parse_args(sys.argv[1:] + ['--help'])

    def modify_parser(self):
        self.parser.description = '''
            This is master control file of the coding-analysis framework.'''


def run():
    MainParser().main()
