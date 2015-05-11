import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseLanguage(AnalyserHook):
    @staticmethod
    def analyse(data):
        for row in data:
            if len(row['languages']) != 1:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   row['languages'].pop()]

    def main(self, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        base_module = self._name.split('.')[1]
        os.makedirs(datapath(base_module, 'result'), exist_ok=True)
        usepath = datapath(base_module, 'extract',
                           make_ext('language-{}'.format(year), 'json'))
        outpath = datapath(base_module, 'result',
                           make_ext('language-{}'.format(year), 'txt'))
        result = chain([['pid', 'io', 'uname', 'language']],
                       self.analyse(json.load(open(usepath))))
        write.table(result, open(outpath, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse language used in each subbmited code.'''
