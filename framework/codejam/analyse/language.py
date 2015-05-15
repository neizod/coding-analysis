import os
import json

from framework._utils import AnalyserHook


class CodeJamAnalyseLanguage(AnalyserHook):
    ''' This method will analyse language used in each subbmited code. '''

    @staticmethod
    def analyse(data):
        for row in data:
            if len(row['languages']) != 1:
                continue
            yield [row['pid'], row['io'], row['uname'],
                   row['languages'].pop()]

    @staticmethod
    def prepare_input(year, **_):
        from framework._utils.misc import datapath, make_ext
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        usepath = datapath('codejam', 'extract',
                           make_ext('language', year, 'json'))
        return json.load(open(usepath))

    @staticmethod
    def prepare_output(result, year, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        outpath = datapath('codejam', 'result',
                           make_ext('language', year, 'txt'))
        header = ['pid', 'io', 'uname', 'language']
        write.table(chain([header], result), open(outpath, 'w'))
