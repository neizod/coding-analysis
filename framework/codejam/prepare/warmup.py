import os
import logging

from framework._utils import SubparsersHook, datapath
from framework.codejam._helper import readsource, iter_submission


class CodeJamPrepareWarmup(SubparsersHook):
    def main(self, year, **_):
        for _, pid, io, screen_name in iter_submission(year):
            wc = 0
            directory = datapath('codejam', 'source', pid, io, screen_name)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if os.path.isfile(filepath):
                    wc += len(readsource(filepath))
            logging.info('warm-up: {} {} {} {}'.format(pid, io, screen_name, wc))

    def modify_parser(self):
        self.parser.description = '''
            This method will warmup source code files for futher analysis.'''
