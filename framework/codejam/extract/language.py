import os
import json
import logging

from framework._utils import SubparsersHook, datapath, source
from framework.codejam._helper import iter_submission


class CodeJamExtractLanguage(SubparsersHook):
    def main(self, year, force=False, **_):
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        output_file = datapath('codejam', 'extract', 'language-{}.json'.format(year))
        if not force and os.path.isfile(output_file):
            return logging.warn('output file already exists, aborting.')
        extracted_data = []
        for _, pid, io, screen_name in iter_submission(year):
            directory = datapath('codejam', 'source', pid, io, screen_name)
            logging.info('extracting: %i %i %s', pid, io, screen_name)
            extracted_data += [{
                'pid': pid,
                'io': io,
                'screen_name': screen_name,
                'languages': sorted(source.determine_languages(directory)),
            }]
        with open(datapath('codejam', output_file), 'w') as file:
            json.dump(extracted_data, file, indent=2)


    def modify_parser(self):
        self.parserdescription = '''
            This method will extract name of programming language used
            in each submission.'''
