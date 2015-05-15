import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseCheat(AnalyserHook):
    ''' This method will analyse cyclomatic complexity. '''

    @staticmethod
    def analyse(data):
        from statistics import mean
        for row in data:
            if not row['cyclomatic-complexity']:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   mean(row['cyclomatic-complexity']),
                   max(row['cyclomatic-complexity'])]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath, make_ext
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath('codejam', 'extract',
                           make_ext('cyclomatic-complexity', year, 'json'))
        return json.load(open(usepath))

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('cyclomatic-complexity', year, 'txt'))
        header = ['pid', 'io', 'uname',
                  'mean-cyclomatic-complexity',
                  'max-cyclomatic-complexity']
        write.table(chain([header], result), open(outpath, 'w'))
