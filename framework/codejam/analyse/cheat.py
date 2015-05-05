import os
import json

from framework._utils import SubparsersHook, datapath


class CodeJamAnalyseCheat(SubparsersHook):
    @staticmethod
    def summary_row(answer):
        return '{} {}\n'.format(answer['pid'], len(answer['cheats']))

    def main(self, year, **_):
        os.makedirs(datapath('codejam', 'result'), exist_ok=True)
        with open(datapath('codejam', 'result', 'cheat-{}.txt'.format(year)), 'w') as file:
            file.write('pid nos-cheat\n')
            for answer in json.load(open(datapath('codejam', 'extract', 'cheat-{}.json'.format(year)))):
                file.write(self.summary_row(answer))

    def modify_parser(self):
        self.parser.description = '''
            This method will analyse cheating by copy-paste source code
            from multiple contestants.'''
