import os

from framework._utils import AnalyserHook


class CodeJamPrepareContestProblemName(AnalyserHook):
    ''' This method will prepare data of contest name and problem name for
        futher analysis. '''

    @staticmethod
    def analyse(data):
        for cid, cname, pid, pname in data:
            yield [cid, cname, pid, pname]

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import iter_contest_problem_name
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'result'), exist_ok=True)
        outpath = datapath(base_module, 'result',
                           make_ext('contest-problem-name', year, 'txt'))
        result = chain([['cid', 'cname', 'pid', 'pname']],
                       self.analyse(iter_contest_problem_name(year)))
        write.table(result, open(outpath, 'w'))
