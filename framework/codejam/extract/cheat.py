import os
import json
import logging
from collections import defaultdict

from framework._utils import SubparsersHook, datapath
from framework.codejam._helper import readsource, iter_submission


class CodeJamExtractCheat(SubparsersHook):
    @staticmethod
    def find_plagiarism(contents):
        def compressed(submit):
            fields = ['io', 'screen_name']
            return {key: value for key, value in submit.items() if key in fields}
        plag_set = defaultdict(list)
        for submits in contents.values():
            if len({submit['screen_name'] for submit in submits}) > 1:
                pid = next(submit['pid'] for submit in submits)
                plag_set[pid] += [[compressed(submit) for submit in submits]]
        return [{'pid': pid, 'cheats': cheats} for pid, cheats in plag_set.items()]

    def main(self, year, force=False, **_):
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        output_file = datapath('codejam', 'extract', 'cheat-{}.json'.format(year))
        if not force and os.path.isfile(output_file):
            return
        contents = defaultdict(list)
        for _, pid, io, screen_name in iter_submission(year):
            directory = datapath('codejam', 'source', pid, io, screen_name)
            logging.info('extracting: %i %i %s', pid, io, screen_name)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if not os.path.isfile(filepath):
                    continue
                sourcecode = readsource(filepath)
                if not sourcecode:
                    continue
                contents[sourcecode] += [{'pid': pid, 'io': io, 'screen_name': screen_name}]
        extracted_data = self.find_plagiarism(contents)
        with open(output_file, 'w') as file:
            json.dump(extracted_data, file, indent=2)

    def modify_parser(self):
        self.parser.description = '''
            This method will extract set of duplicated source codes.'''
