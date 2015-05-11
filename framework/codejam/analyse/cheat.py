import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseCheat(AnalyserHook):
    @staticmethod
    def analyse(data):
        for row in data:
            yield [row['pid'], len(row['cheats'])]

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import datapath, make_ext, write
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'result'), exist_ok=True)
        usepath = datapath(base_module, 'extract',
                           make_ext('cheat-{}'.format(year), 'json'))
        outpath = datapath(base_module, 'result',
                           make_ext('cheat-{}'.format(year), 'txt'))
        result = chain([['pid', 'nos-cheat']],
                       self.analyse(json.load(open(usepath))))
        write.table(result, open(outpath, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse cheating by copy-paste source code
            from multiple contestants.'''
