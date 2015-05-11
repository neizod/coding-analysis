import os
import logging

from framework._utils import FunctionHook


class CodeJamPrepareWarmup(FunctionHook):
    ''' This method will warmup source code files for futher analysis. '''

    def main(self, year, **_):
        from framework._utils.misc import datapath
        from framework.codejam._helper import readsource, iter_submission
        for _, pid, pio, uname in iter_submission(year):
            count = 0
            directory = datapath('codejam', 'source', pid, pio, uname)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if os.path.isfile(filepath):
                    count += len(readsource(filepath))
            logging.info('warm-up: %i %i %s %i', pid, pio, uname, count)
