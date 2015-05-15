import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseIdentifierReadable(AnalyserHook):
    ''' This method will analyse identifier readable from extracted data
        of submitted Google Code Jam source code. '''

    @staticmethod
    def analyse(data):
        from statistics import mean
        from framework._utils.source import Identifier
        mean_readable = lambda idens: (
            mean(int(Identifier(iden).readable()) for iden in idens))
        for row in data:
            if not row['identifiers']:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   mean_readable(row['identifiers'])]

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
                           make_ext('identifier-readable', year, 'txt'))
        header = ['pid', 'io', 'uname', 'identifier-readable']
        write.table(chain([header], result), open(outpath, 'w'))
