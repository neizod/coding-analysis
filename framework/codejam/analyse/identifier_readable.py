import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseIdentifierReadable(AnalyserHook):
    @staticmethod
    def analyse(data):
        from framework._utils.source import Identifier
        mean_readable = lambda identifiers: (
            sum(Identifier(iden).readable() for iden in identifiers) //
            len(identifiers))
        for row in data:
            if not row['identifiers']:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   mean_readable(row['identifiers'])]

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import datapath, make_ext, write
        base_module = self._name.split('.')[1]
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath(base_module, 'extract',
                           make_ext('identifier-{}'.format(year), 'json'))
        outpath = datapath(base_module, 'result',
                           make_ext('identifier-readable-{}'.format(year), 'txt'))
        result = chain([['pid', 'io', 'uname', 'identifier-readable']],
                       self.analyse(json.load(open(usepath))))
        write.table(result, open(outpath, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse identifier readable from extracted data
            of submitted Google Code Jam source code.'''
