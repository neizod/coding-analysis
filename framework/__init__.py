import logging
import sys

from framework._utils import SubmodulesHook


class RootParser(SubmodulesHook):
    def main(self):
        args = self.parser.parse_args()
        if 'function' in args:
            logging.basicConfig(level=args.quiet)
            args.function(**vars(args))
        else:
            self.parser.parse_args(sys.argv[1:] + ['--help'])

    def modify_parser(self):
        self.parser.description = '''
            This is master control file of the coding-analysis framework.'''


def run():
    RootParser().main()
