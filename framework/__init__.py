import sys
import logging

from framework._utils import SubmodulesHook


class RootParser(SubmodulesHook):
    ''' This is master control for the coding-analysis framework. '''

    def run(self):
        ''' excute function if specify, otherwise try to show full help. '''
        args = self.parser.parse_args()
        if 'function' in args:
            logging.basicConfig(level=args.quiet)
            args.function(**vars(args))
        else:
            self.parser.parse_args(sys.argv[1:] + ['--help'])


def run():
    ''' simple interface for outside script to call the framework. '''
    RootParser().run()
