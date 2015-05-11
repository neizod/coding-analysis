import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseIdentifierLength(AnalyserHook):
    @staticmethod
    def analyse(data):
        import statistics as stat
        for row in data:
            if not row['identifiers']:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   stat.mean(len(iden) for iden in row['identifiers'])]

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        base_module = self._name.split('.')[1]
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath(base_module, 'extract',
                           make_ext('identifier', year, 'json'))
        outpath = datapath(base_module, 'result',
                           make_ext('identifier-length', year, 'txt'))
        result = chain([['pid', 'io', 'uname', 'identifier-length']],
                       self.analyse(json.load(open(usepath))))
        write.table(result, open(outpath, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse identifier length from extracted data
            of submitted Google Code Jam source code.'''
