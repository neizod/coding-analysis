import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseIdentifierLength(AnalyserHook):
    ''' This method will analyse identifier length from extracted data of
        submitted Google Code Jam source code. '''

    @staticmethod
    def analyse(data):
        from  statistics import mean
        for row in data:
            if not row['identifiers']:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   mean(len(iden) for iden in row['identifiers'])]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath, make_ext
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath('codejam', 'extract',
                           make_ext('identifier', year, 'json'))
        return json.load(open(usepath))

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('identifier-length', year, 'txt'))
        header = ['pid', 'io', 'uname', 'identifier-length']
        write.table(chain([header], result), open(outpath, 'w'))
