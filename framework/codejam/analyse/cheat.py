import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseCheat(AnalyserHook):
    ''' This method will analyse cheating by copy-paste source code in
        multiple contestants. '''

    @staticmethod
    def analyse(data):
        for row in data:
            yield [row['pid'], len(row['cheats'])]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath, make_ext
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath('codejam', 'extract',
                           make_ext('cheat', year, 'json'))
        return json.load(open(usepath))

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('cheat', year, 'txt'))
        header = ['pid', 'nos-cheat']
        write.table(chain([header], result), open(outpath, 'w'))
