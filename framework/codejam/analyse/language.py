import os
import json

from framework._utils import FunctionHook


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


class CodeJamAnalyseLanguage(FunctionHook):
    @staticmethod
    def summary_row(answer):
        if len(answer['languages']) != 1:
            return ''
        return '{} {} {} {}\n'.format(answer['pid'],
                                      answer['io'],
                                      answer['screen_name'],
                                      repr_or_na(answer['languages'].pop()))

    def main(self, year, **_):
        from framework._utils import datapath
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        with open(datapath('codejam', 'result', 'language-{}.txt'.format(year)), 'w') as file:
            file.write('pid io screen_name language\n')
            for answer in json.load(open(datapath('codejam', 'extract', 'language-{}.json'.format(year)))):
                file.write(self.summary_row(answer))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse language used in each subbmited code.'''
