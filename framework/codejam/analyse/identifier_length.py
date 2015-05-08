import os
import json

from framework._utils import FunctionHook


class CodeJamAnalyseIdentifierLength(FunctionHook):
    @staticmethod
    def summary_row(answer):
        import statistics as stat
        if not answer['identifiers']:
            mean = None
        else:
            mean = stat.mean(len(iden) for iden in answer['identifiers'])
        return '{} {} {} {}\n'.format(answer['pid'],
                                      answer['io'],
                                      answer['screen_name'],
                                      mean)

    def main(self, year, **_):
        from framework._utils import datapath
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        with open(datapath('codejam', 'result', 'identifier-length-{}.txt'.format(year)), 'w') as file:
            file.write('pid io screen_name identifier-length\n')
            for answer in json.load(open(datapath('codejam', 'extract', 'identifier-{}.json'.format(year)))):
                file.write(self.summary_row(answer))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse identifier length from extracted data
            of submitted Google Code Jam source code.'''
