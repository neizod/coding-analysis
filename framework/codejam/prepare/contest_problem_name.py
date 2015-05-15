import os

from framework._utils import AnalyserHook


class CodeJamPrepareContestProblemName(AnalyserHook):
    ''' This method will prepare data of contest name and problem name for
        futher analysis. '''

    @staticmethod
    def analyse(data):
        for cid, cname, pid, pname in data:
            yield [cid, cname, pid, pname]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath
        from framework.codejam._helper import iter_contest_problem_name
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        return iter_contest_problem_name(year)

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('contest-problem-name', year, 'txt'))
        header = ['cid', 'cname', 'pid', 'pname']
        write.table(chain([header], result), open(outpath, 'w'))
