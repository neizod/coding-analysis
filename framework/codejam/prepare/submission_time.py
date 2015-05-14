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

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import iter_all_attempt
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'result'), exist_ok=True)
        outpath = datapath(base_module, 'result',
                           make_ext('submission-time', year, 'txt'))
        result = chain([['pid', 'io', 'uname', 'submission-time']],
                       self.analyse(iter_all_attempt(year)))
        write.table(result, open(outpath, 'w'))
