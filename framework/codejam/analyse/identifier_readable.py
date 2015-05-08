import os
import json

from framework._utils import FunctionHook


def repr_or_na(data):
    return repr(data) if data is not None else 'NA'


class CodeJamAnalyseIdentifierReadable(FunctionHook):
    @staticmethod
    def summary_row(answer):
        from framework._utils import source
        if not answer['identifiers']:
            mean = None
        else:
            mean = sum(source.Identifier(string).readable() for string in answer['identifiers']) / len(answer['identifiers'])
        return '{} {} {} {}\n'.format(answer['pid'],
                                      answer['io'],
                                      answer['screen_name'],
                                      repr_or_na(mean))

    def main(self, year, **_):
        from framework._utils import datapath
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        with open(datapath('codejam', 'result', 'identifier-readable-{}.txt'.format(year)), 'w') as file:
            file.write('pid io screen_name identifier-readable\n')
            for answer in json.load(open(datapath('codejam', 'extract', 'identifier-{}.json'.format(year)))):
                file.write(self.summary_row(answer))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse identifier readable from extracted data
            of submitted Google Code Jam source code.'''
