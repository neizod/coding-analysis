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

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'result'), exist_ok=True)
        usepath = datapath(base_module, 'extract',
                           make_ext('cyclomatic-complexity', year, 'json'))
        outpath = datapath(base_module, 'result',
                           make_ext('cyclomatic-complexity', year, 'txt'))
        result = chain([['pid', 'io', 'uname',
                         'mean-cyclomatic-complexity',
                         'max-cyclomatic-complexity']],
                       self.analyse(json.load(open(usepath))))
        write.table(result, open(outpath, 'w'))
