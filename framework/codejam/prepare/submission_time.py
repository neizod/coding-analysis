import os

from framework._utils import AnalyserHook


class CodeJamPrepareSubmissionTime(AnalyserHook):
    ''' This method will prepare data of submission time. '''

    @staticmethod
    def analyse(data):
        for _, uname, pid, pio, _, submission_time in data:
            if submission_time == -1:
                continue
            yield [pid, pio, uname, submission_time]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath
        from framework.codejam._helper import iter_all_attempt
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        return iter_all_attempt(year)

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('submission-time', year, 'txt'))
        header = ['pid', 'io', 'uname', 'submission-time']
        write.table(chain([header], result), open(outpath, 'w'))
