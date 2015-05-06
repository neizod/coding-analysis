import os
import json
from itertools import chain

from framework._utils import AnalyserHook, datapath, write


class CodeJamAnalyseCheat(AnalyserHook):
    @staticmethod
    def analyse(data):
        for row in data:
            yield [row['pid'], len(row['cheats'])]

    def main(self, year, **_):
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'analyse'), exist_ok=True)
        extract_filepath = datapath(base_module, 'extract', 'cheat-{}.json'.format(year))
        analyse_filepath = datapath(base_module, 'analyse', 'cheat-{}.txt'.format(year))
        output = chain([['pid', 'nos-cheat']], self.analyse(json.load(open(extract_filepath))))
        write.table(output, open(analyse_filepath, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse cheating by copy-paste source code
            from multiple contestants.'''
